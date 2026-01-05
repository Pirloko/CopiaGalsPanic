import Phaser from 'phaser';
import { Enemy } from '../entities/Enemy';
import { EnemyType, ENEMY_CONFIG, GAME_CONFIG, PLAYER_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';
import { Geometry, Point } from '../utils/geometry';
import { LineDrawer } from './LineDrawer';
import { PolygonFiller } from './PolygonFiller';

/**
 * Sistema de gestión de enemigos
 * Maneja spawn, actualización y colisiones de enemigos
 */
export class EnemyManager {
  private scene: Phaser.Scene;
  private enemies: Enemy[] = [];
  private player?: Phaser.GameObjects.GameObject;
  private lineDrawer?: LineDrawer;
  private polygonFiller?: PolygonFiller;
  private spawnTimer?: Phaser.Time.TimerEvent;
  private capturedEnemies: Set<Enemy> = new Set(); // Enemigos ya capturados
  private slowMultiplier: number = 1.0; // Multiplicador de velocidad (para efecto slow)
  private isFrozen: boolean = false; // Si los enemigos están congelados
  private freezeTimer?: Phaser.Time.TimerEvent;
  private slowTimer?: Phaser.Time.TimerEvent;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
  }

  /**
   * Establece la referencia al jugador
   */
  public setPlayer(player: Phaser.GameObjects.GameObject): void {
    this.player = player;
    // Actualizar target de todos los enemigos existentes
    this.enemies.forEach(enemy => enemy.setTarget(player));
  }

  /**
   * Establece la referencia al LineDrawer
   */
  public setLineDrawer(lineDrawer: LineDrawer): void {
    this.lineDrawer = lineDrawer;
  }

  /**
   * Establece la referencia al PolygonFiller
   */
  public setPolygonFiller(polygonFiller: PolygonFiller): void {
    this.polygonFiller = polygonFiller;
  }

  /**
   * Inicia el sistema de spawn de enemigos
   */
  public startSpawning(): void {
    
    // Spawn inicial
    this.spawnEnemy();

    // Configurar spawn periódico
    this.spawnTimer = this.scene.time.addEvent({
      delay: ENEMY_CONFIG.SPAWN_INTERVAL,
      callback: this.spawnEnemy,
      callbackScope: this,
      loop: true,
    });
  }

  /**
   * Detiene el sistema de spawn
   */
  public stopSpawning(): void {
    if (this.spawnTimer) {
      this.spawnTimer.destroy();
      this.spawnTimer = undefined;
    }
  }

  /**
   * Genera un enemigo en una posición aleatoria
   */
  private spawnEnemy(): void {
    // Verificar límite de enemigos activos
    if (this.enemies.length >= GAME_CONFIG.MAX_ENEMIES_ACTIVE) {
      return;
    }

    // Posición aleatoria dentro del área de juego
    const x = Phaser.Math.Between(
      ENEMY_CONFIG.SIZE,
      GAME_CONFIG.GAME_AREA_WIDTH - ENEMY_CONFIG.SIZE
    );
    const y = Phaser.Math.Between(
      ENEMY_CONFIG.SIZE,
      GAME_CONFIG.GAME_AREA_HEIGHT - ENEMY_CONFIG.SIZE
    );

    // Seleccionar tipo aleatorio (todos los tipos disponibles)
    const types = [
      EnemyType.RANDOM,
      EnemyType.SLOW_CHASER,
      EnemyType.BOUNCE,
      EnemyType.FAST_CHASER,
      EnemyType.COMBINED,
    ];
    const type = Phaser.Math.RND.pick(types);

    const enemy = new Enemy(this.scene, x, y, type);

    // Configurar target si es perseguidor
    if (this.player && (type === EnemyType.SLOW_CHASER || type === EnemyType.FAST_CHASER)) {
      enemy.setTarget(this.player);
    }

    this.enemies.push(enemy);

    // Emitir evento
    this.scene.events.emit(GameEvents.ENEMY_SPAWNED, {
      enemy: enemy,
      type: type,
    });
  }

  /**
   * Actualiza todos los enemigos
   */
  public update(delta: number): void {
    // Si están congelados, no actualizar
    if (this.isFrozen) {
      return;
    }

    // Actualizar cada enemigo
    this.enemies.forEach(enemy => {
      // Solo actualizar si no está capturado
      if (!this.capturedEnemies.has(enemy)) {
        // Aplicar multiplicador de velocidad (para efecto slow)
        const adjustedDelta = delta * this.slowMultiplier;
        enemy.update(adjustedDelta, this.player);

        // Verificar colisión con líneas
        this.checkLineCollision(enemy);

        // Verificar colisión con polígonos cerrados
        this.checkPolygonCollision(enemy);
      }
    });

    // Verificar colisiones con jugador (solo enemigos no capturados)
    if (this.player) {
      this.checkPlayerCollision();
    }
  }

  /**
   * Verifica colisiones entre enemigos y líneas dibujadas
   */
  private checkLineCollision(enemy: Enemy): void {
    if (!this.lineDrawer) return;

    const points = this.lineDrawer.getPoints();
    if (points.length < 2) return;

    const enemyPos = { x: enemy.x, y: enemy.y };
    const enemyRadius = ENEMY_CONFIG.SIZE;

    // Verificar colisión con cada segmento de línea
    for (let i = 0; i < points.length - 1; i++) {
      const lineStart = points[i];
      const lineEnd = points[i + 1];

      if (Geometry.lineCircleCollision(lineStart, lineEnd, enemyPos, enemyRadius)) {
        // Colisión detectada: borrar la línea
        this.lineDrawer.clearLine();
        
        // Emitir evento (opcional, para efectos visuales/sonidos)
        this.scene.events.emit(GameEvents.ENEMY_DESTROYED, {
          enemy: enemy,
          reason: 'line_collision',
        });

        // El enemigo continúa (no se destruye por colisión con línea)
        break;
      }
    }
  }

  /**
   * Verifica colisiones entre enemigos y el jugador
   */
  private checkPlayerCollision(): void {
    if (!this.player) return;

    this.enemies.forEach(enemy => {
      // Ignorar enemigos capturados
      if (this.capturedEnemies.has(enemy)) return;

      if (!this.player) return;
      const playerX = 'x' in this.player ? (this.player as any).x : 0;
      const playerY = 'y' in this.player ? (this.player as any).y : 0;
      const distance = Phaser.Math.Distance.Between(
        enemy.x,
        enemy.y,
        playerX,
        playerY
      );

      const minDistance = ENEMY_CONFIG.SIZE + PLAYER_CONFIG.SIZE;

      if (distance < minDistance) {
        // Colisión detectada
        this.scene.events.emit(GameEvents.PLAYER_HIT, {
          enemy: enemy,
        });
      }
    });
  }

  /**
   * Verifica colisiones entre enemigos y polígonos cerrados
   */
  private checkPolygonCollision(enemy: Enemy): void {
    if (!this.polygonFiller) return;
    if (this.capturedEnemies.has(enemy)) return;

    const polygons = this.polygonFiller.getPolygons();
    const enemyPos: Point = { x: enemy.x, y: enemy.y };

    // Verificar si el enemigo está dentro de algún polígono
    for (const polygon of polygons) {
      if (Geometry.pointInPolygon(enemyPos, polygon)) {
        // Enemigo atrapado en polígono
        this.captureEnemy(enemy);
        break;
      }
    }
  }

  /**
   * Captura un enemigo (lo destruye y da puntos)
   */
  private captureEnemy(enemy: Enemy): void {
    if (this.capturedEnemies.has(enemy)) return;

    this.capturedEnemies.add(enemy);

    // Remover de la lista y destruir
    const index = this.enemies.indexOf(enemy);
    if (index !== -1) {
      this.enemies.splice(index, 1);
      enemy.destroy();

      // Emitir evento con información de captura y puntos
      this.scene.events.emit(GameEvents.ENEMY_DESTROYED, {
        enemy: enemy,
        reason: 'captured',
        points: ENEMY_CONFIG.POINTS_PER_CAPTURED_ENEMY,
      });
    }
  }

  /**
   * Destruye un enemigo específico
   */
  public destroyEnemy(enemy: Enemy): void {
    if (this.capturedEnemies.has(enemy)) return; // Ya fue capturado

    const index = this.enemies.indexOf(enemy);
    if (index !== -1) {
      this.enemies.splice(index, 1);
      enemy.destroy();

      this.scene.events.emit(GameEvents.ENEMY_DESTROYED, {
        enemy: enemy,
        reason: 'destroyed',
      });
    }
  }

  /**
   * Obtiene todos los enemigos activos
   */
  public getEnemies(): Enemy[] {
    return [...this.enemies];
  }

  /**
   * Limpia todos los enemigos
   */
  public clearAll(): void {
    this.enemies.forEach(enemy => enemy.destroy());
    this.enemies = [];
    this.capturedEnemies.clear();
  }

  /**
   * Aplica efecto de ralentización a todos los enemigos
   */
  public applySlowEffect(duration: number, multiplier: number): void {
    // Limpiar timer anterior si existe
    if (this.slowTimer) {
      this.slowTimer.destroy();
    }

    this.slowMultiplier = multiplier;

    this.slowTimer = this.scene.time.delayedCall(duration, () => {
      this.slowMultiplier = 1.0;
      this.slowTimer = undefined;
    });
  }

  /**
   * Aplica efecto de congelación a todos los enemigos
   */
  public applyFreezeEffect(duration: number): void {
    // Limpiar timer anterior si existe
    if (this.freezeTimer) {
      this.freezeTimer.destroy();
    }

    this.isFrozen = true;

    this.freezeTimer = this.scene.time.delayedCall(duration, () => {
      this.isFrozen = false;
      this.freezeTimer = undefined;
    });
  }

  /**
   * Destruye todos los enemigos (efecto bomba)
   */
  public destroyAllEnemies(): void {
    const enemiesToDestroy = [...this.enemies];
    enemiesToDestroy.forEach(enemy => {
      if (!this.capturedEnemies.has(enemy)) {
        this.destroyEnemy(enemy);
      }
    });
  }

  /**
   * Resetea el sistema
   */
  public reset(): void {
    this.stopSpawning();
    this.clearAll();
    
    // Limpiar efectos
    if (this.freezeTimer) {
      this.freezeTimer.destroy();
      this.freezeTimer = undefined;
    }
    if (this.slowTimer) {
      this.slowTimer.destroy();
      this.slowTimer = undefined;
    }
    this.isFrozen = false;
    this.slowMultiplier = 1.0;
  }
}
