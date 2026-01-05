import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';

/**
 * Botón para activar/desactivar el modo de dibujo
 */
export class DrawButton {
  private scene: Phaser.Scene;
  private button!: Phaser.GameObjects.Container;
  private background!: Phaser.GameObjects.Rectangle;
  private icon!: Phaser.GameObjects.Text;
  private isActive: boolean = false;
  private buttonX: number = 0;
  private buttonY: number = 0;
  private width: number = 80;
  private height: number = 80;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.setupButton();
  }

  /**
   * Configura el botón
   */
  private setupButton(): void {
    // Posición: lado derecho, cerca del joystick (debajo del área de juego)
    const screenHeight = this.scene.cameras.main.height;
    const screenWidth = this.scene.cameras.main.width;
    this.buttonX = screenWidth - 120; // 120px desde el borde derecho
    this.buttonY = screenHeight - 100; // 100px desde el borde inferior (misma altura que joystick)

    // Crear contenedor
    this.button = this.scene.add.container(this.buttonX, this.buttonY);

    // Fondo del botón (rectángulo redondeado)
    this.background = this.scene.add.rectangle(
      0,
      0,
      this.width,
      this.height,
      0x333333,
      0.8
    );
    this.background.setStrokeStyle(3, 0xffffff);
    this.background.setInteractive({ useHandCursor: true });

    // Ícono/texto del botón
    this.icon = this.scene.add.text(0, 0, '✎', {
      fontSize: '40px',
      fontFamily: 'Arial',
      color: '#ffffff',
    });
    this.icon.setOrigin(0.5);

    // Añadir elementos al contenedor
    this.button.add([this.background, this.icon]);
    this.button.setScrollFactor(0); // Fijar en la cámara
    this.button.setDepth(1000);

    // Eventos
    this.background.on('pointerdown', () => {
      this.toggle();
    });

    // Actualizar estado visual inicial
    this.updateVisualState();
  }

  /**
   * Alterna el estado activo/inactivo
   */
  public toggle(): void {
    this.isActive = !this.isActive;
    this.updateVisualState();
    
    // Emitir evento para que GameScene lo escuche
    this.scene.events.emit('drawModeToggled', { active: this.isActive });
  }

  /**
   * Establece el estado activo
   */
  public setActive(active: boolean): void {
    this.isActive = active;
    this.updateVisualState();
  }

  /**
   * Obtiene el estado activo
   */
  public getActive(): boolean {
    return this.isActive;
  }

  /**
   * Actualiza el estado visual del botón
   */
  private updateVisualState(): void {
    if (this.isActive) {
      // Modo activo: verde con borde más grueso
      this.background.setFillStyle(0x00ff00, 0.8);
      this.background.setStrokeStyle(4, 0x00aa00);
      this.icon.setColor('#000000');
    } else {
      // Modo inactivo: gris
      this.background.setFillStyle(0x333333, 0.8);
      this.background.setStrokeStyle(3, 0xffffff);
      this.icon.setColor('#ffffff');
    }
  }

  /**
   * Muestra/oculta el botón
   */
  public setVisible(visible: boolean): void {
    this.button.setVisible(visible);
  }

  /**
   * Limpia recursos
   */
  public destroy(): void {
    this.button.destroy();
  }
}

