import Phaser from 'phaser';
import { Player } from '../entities/Player';
import { GAME_CONFIG, PLAYER_CONFIG, POWERUP_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';
import { PowerUpType } from '../config/gameConfig';
import { LineDrawer } from '../systems/LineDrawer';
import { PolygonFiller } from '../systems/PolygonFiller';
import { LevelManager } from '../systems/LevelManager';
import { TimeManager } from '../systems/TimeManager';
import { ScoreManager } from '../systems/ScoreManager';
import { LivesManager } from '../systems/LivesManager';
import { EnemyManager } from '../systems/EnemyManager';
import { PowerUpManager } from '../systems/PowerUpManager';
import { AudioManager } from '../systems/AudioManager';
import { HUD } from '../ui/HUD';

/**
 * Escena principal del juego
 * Orquesta todos los sistemas y entidades
 */
export class GameScene extends Phaser.Scene {
  private player!: Player;
  private lineDrawer!: LineDrawer;
  private polygonFiller!: PolygonFiller;
  private levelManager!: LevelManager;
  private timeManager!: TimeManager;
  private scoreManager!: ScoreManager;
  private livesManager!: LivesManager;
  private enemyManager!: EnemyManager;
  private powerUpManager!: PowerUpManager;
  private audioManager!: AudioManager;
  private hud!: HUD;
  
  // Datos del juego (para pasar entre scenes)
  private gameData: {
    level: number;
    score: number;
  } = { level: 1, score: 0 };

  constructor() {
    super({ key: 'GameScene' });
  }

  init(data?: { level?: number }): void {
    // Recibir datos de nivel inicial (si viene de otra scene)
    if (data && data.level) {
      this.gameData.level = data.level;
    }
  }

  create(): void {
    // Configurar física
    this.physics.world.setBounds(
      0,
      0,
      GAME_CONFIG.GAME_AREA_WIDTH,
      GAME_CONFIG.GAME_AREA_HEIGHT
    );

    // Área de juego (borde visual)
    this.add.rectangle(
      GAME_CONFIG.GAME_AREA_WIDTH / 2,
      GAME_CONFIG.GAME_AREA_HEIGHT / 2,
      GAME_CONFIG.GAME_AREA_WIDTH,
      GAME_CONFIG.GAME_AREA_HEIGHT,
      0x2a2a2a,
      0
    ).setStrokeStyle(2, 0xffffff);

    // Área HUD (placeholder visual)
    this.add.rectangle(
      GAME_CONFIG.GAME_AREA_WIDTH + GAME_CONFIG.HUD_WIDTH / 2,
      GAME_CONFIG.HEIGHT / 2,
      GAME_CONFIG.HUD_WIDTH,
      GAME_CONFIG.HUD_HEIGHT,
      0x1a1a1a
    ).setStrokeStyle(2, 0x666666);

    // Detectar si es móvil/táctil
    const isMobile = (globalThis as any).__GAME_IS_MOBILE__ || false;
    const isTouch = (globalThis as any).__GAME_IS_TOUCH__ || false;
    const useTouchControls = isMobile || isTouch;

    // Crear jugador
    this.player = new Player(
      this,
      PLAYER_CONFIG.START_X,
      PLAYER_CONFIG.START_Y,
      useTouchControls
    );

    // Inicializar sistemas
    this.lineDrawer = new LineDrawer(this);
    this.polygonFiller = new PolygonFiller(this);
    this.levelManager = new LevelManager(this, this.gameData.level);
    this.timeManager = new TimeManager(this);
    this.scoreManager = new ScoreManager(this);
    this.livesManager = new LivesManager(this);
    this.enemyManager = new EnemyManager(this);
    this.powerUpManager = new PowerUpManager(this);
    this.audioManager = new AudioManager(this);
    this.audioManager.init(); // Inicializar audio (preparado para sonidos futuros)
    this.hud = new HUD(this);

    // Configurar referencias entre sistemas
    this.enemyManager.setPlayer(this.player);
    this.enemyManager.setLineDrawer(this.lineDrawer);
    this.enemyManager.setPolygonFiller(this.polygonFiller);
    this.powerUpManager.setPlayer(this.player);

    // Configurar eventos
    this.setupEvents();

    // Iniciar juego
    this.startLevel(this.gameData.level);
  }

  /**
   * Configura los listeners de eventos globales
   */
  private setupEvents(): void {
    // Evento cuando se cierra un área (polígono válido)
    this.events.on(GameEvents.AREA_CLOSED, (data: { vertices: any[]; area: number }) => {
      // Rellenar el polígono
      this.polygonFiller.fillPolygon(data.vertices);
    });

    // Evento cuando se valida un polígono (después del rellenado)
    this.events.on(
      GameEvents.POLYGON_VALIDATED,
      (data: { vertices: any[]; area: number; totalArea: number; percentage: number }) => {
        // Añadir puntaje por área cerrada
        this.scoreManager.addAreaScore(data.area, data.vertices.length);

        // Verificar si el nivel está completo
        this.levelManager.checkLevelComplete(data.percentage);

        // Actualizar HUD
        this.updateHUD();
      }
    );

    // Evento cuando se completa un nivel
    this.events.on(
      GameEvents.LEVEL_COMPLETE,
      (data: { level: number; percentage: number; requiredPercentage: number }) => {
        // Añadir bonificación por completar nivel
        this.scoreManager.addLevelCompleteBonus(data.level);

        // Añadir bonificación por tiempo restante
        const timeRemaining = this.timeManager.getCurrentTime();
        this.scoreManager.addTimeBonus(timeRemaining);

        // Actualizar puntaje
        this.gameData.score = this.scoreManager.getScore();

        // Pausar temporizador
        this.timeManager.stopTimer();

        // Reproducir sonido de victoria
        this.audioManager.playVictory();

        // Ir a scene de nivel completado
        this.scene.start('LevelCompleteScene', {
          level: data.level,
          score: this.gameData.score,
          nextLevel: data.level < GAME_CONFIG.MAX_LEVELS ? data.level + 1 : undefined,
        });
      }
    );

    // Evento cuando se inicia un nivel
    this.events.on(GameEvents.LEVEL_START, (data: { level: number; requiredPercentage: number }) => {
      this.hud.updateLevel(data.level);
      this.updateHUD();
    });

    // Evento Game Over
    this.events.on(GameEvents.GAME_OVER, (data: { reason: string; level?: number }) => {
      this.timeManager.stopTimer();
      this.gameData.score = this.scoreManager.getScore();
      
      // Ir a scene de game over
      this.scene.start('GameOverScene', {
        score: this.gameData.score,
        level: this.levelManager.getCurrentLevel(),
        reason: data.reason,
      });
    });

    // Evento cuando el jugador es golpeado por un enemigo
    this.events.on(GameEvents.PLAYER_HIT, () => {
      // Solo procesar si el jugador no es invulnerable
      if (!this.player.getInvulnerable()) {
        // Hacer invulnerable temporalmente
        this.player.setInvulnerable();
        
        // Reproducir sonido de daño
        this.audioManager.playHit();
        
        // Reducir una vida
        this.livesManager.loseLife();
      }
    });

    // Evento cuando un enemigo es destruido/capturado
    this.events.on(GameEvents.ENEMY_DESTROYED, (data: { enemy: any; reason: string; points?: number }) => {
      if (data.reason === 'captured' && data.points) {
        // Añadir puntos por enemigo capturado
        this.scoreManager.setScore(this.scoreManager.getScore() + data.points);
      }
    });

    // Evento cuando se recolecta un power-up
    this.events.on(GameEvents.POWERUP_COLLECTED, (data: { type: PowerUpType; typeName: string }) => {
      // Reproducir sonido de power-up
      this.audioManager.playPowerUp();
      this.applyPowerUpEffect(data.type);
    });
  }

  /**
   * Inicia un nivel
   */
  private startLevel(level: number): void {
    // Actualizar datos del juego
    this.gameData.level = level;

    // Si es nivel 1, resetear puntaje y vidas
    if (level === 1) {
      this.scoreManager.reset();
      this.livesManager.reset();
      this.gameData.score = 0;
    }

    // Resetear sistemas necesarios
    this.polygonFiller.reset();
    this.levelManager.reset(level);
    this.lineDrawer.clearLine();
    this.enemyManager.reset();
    this.powerUpManager.reset();

    // Iniciar temporizador
    this.timeManager.startTimer(level);

    // Iniciar spawn de enemigos y power-ups
    this.enemyManager.startSpawning();
    this.powerUpManager.startSpawning();

    // Reproducir música de fondo (si está disponible)
    this.audioManager.playMusic();

    // Emitir evento de inicio de nivel
    this.events.emit(GameEvents.LEVEL_START, {
      level: level,
      requiredPercentage: this.levelManager.getRequiredPercentage(),
    });

    // Actualizar HUD
    this.updateHUD();
  }

  /**
   * Aplica el efecto de un power-up recolectado
   */
  private applyPowerUpEffect(type: PowerUpType): void {
    switch (type) {
      case PowerUpType.SHIELD:
        // Escudo: Jugador invulnerable
        this.player.setInvulnerable(POWERUP_CONFIG.SHIELD_DURATION);
        break;

      case PowerUpType.SLOW:
        // Ralentización: Enemigos más lentos
        this.enemyManager.applySlowEffect(
          POWERUP_CONFIG.SLOW_DURATION,
          POWERUP_CONFIG.SLOW_MULTIPLIER
        );
        break;

      case PowerUpType.FREEZE:
        // Congelación: Enemigos detenidos
        this.enemyManager.applyFreezeEffect(POWERUP_CONFIG.FREEZE_DURATION);
        break;

      case PowerUpType.EXTRA_LIFE:
        // Vida Extra: Añade una vida
        this.livesManager.addLife();
        break;

      case PowerUpType.BOMB:
        // Bomba: Destruye todos los enemigos
        this.audioManager.playExplosion();
        this.enemyManager.destroyAllEnemies();
        break;
    }
  }

  /**
   * Actualiza el HUD con la información actual
   */
  private updateHUD(): void {
    const revealedPercentage = this.polygonFiller.getRevealedPercentage();
    const requiredPercentage = this.levelManager.getRequiredPercentage();
    this.hud.updatePercentage(revealedPercentage, requiredPercentage);
  }

  update(_time: number, delta: number): void {
    // Actualizar jugador
    this.player.update(delta);

    // Actualizar sistemas
    this.lineDrawer.update(delta);
    this.enemyManager.update(delta);
    this.powerUpManager.update(delta);
  }
}
