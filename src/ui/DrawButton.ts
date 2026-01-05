import Phaser from 'phaser';

/**
 * Botón para activar/desactivar el modo de trazado
 */
export class DrawButton {
  private scene: Phaser.Scene;
  private button!: Phaser.GameObjects.Container;
  private background!: Phaser.GameObjects.Arc;
  private icon!: Phaser.GameObjects.Text;
  private isActive: boolean = false;
  private x: number;
  private y: number;
  private radius: number = 50;

  constructor(scene: Phaser.Scene, x: number, y: number) {
    this.scene = scene;
    this.x = x;
    this.y = y;
    this.create();
  }

  /**
   * Crea los elementos visuales del botón
   */
  private create(): void {
    // Contenedor para agrupar el botón
    this.button = this.scene.add.container(this.x, this.y);

    // Fondo del botón
    this.background = this.scene.add.circle(0, 0, this.radius, 0x333333, 0.8);
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
