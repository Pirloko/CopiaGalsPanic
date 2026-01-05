import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';

/**
 * Joystick virtual para controles táctiles
 */
export class VirtualJoystick {
  private scene: Phaser.Scene;
  private base!: Phaser.GameObjects.Arc;
  private stick!: Phaser.GameObjects.Arc;
  private isActive: boolean = false;
  private baseX: number = 0;
  private baseY: number = 0;
  private stickX: number = 0;
  private stickY: number = 0;
  private radius: number = 60;
  private stickRadius: number = 25;
  private maxDistance: number = 35;
  
  // Dirección actual (normalizada)
  public direction: Phaser.Math.Vector2 = new Phaser.Math.Vector2(0, 0);
  
  constructor(scene: Phaser.Scene, x?: number, y?: number) {
    this.scene = scene;
    // Si se proporcionan coordenadas, usarlas; sino, usar valores por defecto
    this.baseX = x !== undefined ? x : 100;
    this.baseY = y !== undefined ? y : this.scene.cameras.main.height - 100;
    this.setupJoystick();
  }

  /**
   * Configura el joystick virtual
   */
  private setupJoystick(): void {
    // Usar las coordenadas establecidas en el constructor
    
    // Base del joystick (fondo)
    this.base = this.scene.add.circle(
      this.baseX,
      this.baseY,
      this.radius,
      0x333333,
      0.5
    );
    this.base.setStrokeStyle(2, 0x666666);
    this.base.setInteractive();
    this.base.setScrollFactor(0); // Fijar en la cámara
    this.base.setDepth(1000);
    
    // Stick (control)
    this.stickX = this.baseX;
    this.stickY = this.baseY;
    this.stick = this.scene.add.circle(
      this.stickX,
      this.stickY,
      this.stickRadius,
      0xffffff,
      0.8
    );
    this.stick.setStrokeStyle(2, 0xcccccc);
    this.stick.setScrollFactor(0);
    this.stick.setDepth(1001);
    
    // Eventos táctiles
    this.scene.input.on('pointerdown', this.onPointerDown, this);
    this.scene.input.on('pointermove', this.onPointerMove, this);
    this.scene.input.on('pointerup', this.onPointerUp, this);
  }

  /**
   * Maneja el inicio del toque
   */
  private onPointerDown(pointer: Phaser.Input.Pointer): void {
    // Usar coordenadas de pantalla (no mundo) para el joystick fijo
    const screenX = pointer.x;
    const screenY = pointer.y;
    
    // Verificar si el toque está cerca de la base del joystick
    // Solo activar si está dentro del área del joystick (esquina inferior izquierda)
    const distance = Phaser.Math.Distance.Between(screenX, screenY, this.baseX, this.baseY);
    
    if (distance <= this.radius + 50) {
      // Si el toque está en el área del joystick, activar y prevenir propagación
      this.isActive = true;
      this.updateStickPosition(screenX, screenY);
      // NO prevenir propagación aquí - dejar que otros sistemas también funcionen
    }
  }

  /**
   * Maneja el movimiento del toque
   */
  private onPointerMove(pointer: Phaser.Input.Pointer): void {
    if (!this.isActive) return;
    
    const screenX = pointer.x;
    const screenY = pointer.y;
    this.updateStickPosition(screenX, screenY);
  }

  /**
   * Maneja el fin del toque
   */
  private onPointerUp(): void {
    this.isActive = false;
    this.stick.setPosition(this.baseX, this.baseY);
    this.direction.set(0, 0);
  }

  /**
   * Actualiza la posición del stick y calcula la dirección
   */
  private updateStickPosition(x: number, y: number): void {
    const dx = x - this.baseX;
    const dy = y - this.baseY;
    const distance = Math.sqrt(dx * dx + dy * dy);
    
    if (distance <= this.maxDistance) {
      // Dentro del rango, mover el stick
      this.stickX = x;
      this.stickY = y;
    } else {
      // Limitar a la distancia máxima
      const angle = Math.atan2(dy, dx);
      this.stickX = this.baseX + Math.cos(angle) * this.maxDistance;
      this.stickY = this.baseY + Math.sin(angle) * this.maxDistance;
    }
    
    this.stick.setPosition(this.stickX, this.stickY);
    
    // Calcular dirección normalizada
    const stickDx = this.stickX - this.baseX;
    const stickDy = this.stickY - this.baseY;
    const stickDistance = Math.sqrt(stickDx * stickDx + stickDy * stickDy);
    
    if (stickDistance > 0) {
      this.direction.set(
        stickDx / this.maxDistance,
        stickDy / this.maxDistance
      );
      // Normalizar a máximo 1
      const magnitude = Math.min(1, Math.sqrt(this.direction.x ** 2 + this.direction.y ** 2));
      if (magnitude > 0) {
        this.direction.normalize();
        this.direction.scale(Math.min(1, stickDistance / this.maxDistance));
      }
    } else {
      this.direction.set(0, 0);
    }
  }

  /**
   * Obtiene la dirección horizontal (-1 a 1)
   */
  public getDirectionX(): number {
    return this.direction.x;
  }

  /**
   * Obtiene la dirección vertical (-1 a 1)
   */
  public getDirectionY(): number {
    return this.direction.y;
  }

  /**
   * Muestra/oculta el joystick
   */
  public setVisible(visible: boolean): void {
    this.base.setVisible(visible);
    this.stick.setVisible(visible);
  }

  /**
   * Limpia recursos
   */
  public destroy(): void {
    this.scene.input.off('pointerdown', this.onPointerDown, this);
    this.scene.input.off('pointermove', this.onPointerMove, this);
    this.scene.input.off('pointerup', this.onPointerUp, this);
    this.base.destroy();
    this.stick.destroy();
  }
}

