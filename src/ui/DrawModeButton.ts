import Phaser from 'phaser';

/**
 * Botón para activar/desactivar el modo de dibujo
 */
export class DrawModeButton {
  private scene: Phaser.Scene;
  private button!: Phaser.GameObjects.Container;
  private background!: Phaser.GameObjects.Circle;
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
   * Crea el botón visual
   */
  private create(): void {
    // Fondo del botón
    this.background = this.scene.add.circle(
      this.x,
      this.y,
      this.radius,
      0x444444,
      0.8
    );
    this.background.setStrokeStyle(3, 0x888888, 1);
    this.background.setInteractive({ useHandCursor: true });
    this.background.setScrollFactor(0); // Fijo en la cámara
    this.background.setDepth(1000);

    // Icono (lápiz o X para activar/desactivar)
    this.icon = this.scene.add.text(
      this.x,
      this.y,
      '✎', // Símbolo de lápiz
      {
        fontSize: '32px',
        fontFamily: 'Arial',
        color: '#ffffff',
      }
    );
    this.icon.setOrigin(0.5);
    this.icon.setScrollFactor(0);
    this.icon.setDepth(1001);

    // Container para agrupar
    this.button = this.scene.add.container(this.x, this.y, [
      this.background,
      this.icon,
    ]);
    this.button.setScrollFactor(0);
    this.button.setDepth(1000);
    this.button.setSize(this.radius * 2, this.radius * 2);

    // Evento de click/touch
    this.background.on('pointerdown', () => {
      this.toggle();
    });

    // Actualizar visual
    this.updateVisual();
  }

  /**
   * Activa o desactiva el modo de dibujo
   */
  public toggle(): void {
    this.isActive = !this.isActive;
    this.updateVisual();
    
    // Emitir evento
    this.scene.events.emit('drawModeToggled', this.isActive);
  }

  /**
   * Establece el estado activo
   */
  public setActive(active: boolean): void {
    if (this.isActive !== active) {
      this.isActive = active;
      this.updateVisual();
      this.scene.events.emit('drawModeToggled', this.isActive);
    }
  }

  /**
   * Obtiene el estado activo
   */
  public getActive(): boolean {
    return this.isActive;
  }

  /**
   * Actualiza la apariencia visual del botón
   */
  private updateVisual(): void {
    if (this.isActive) {
      // Modo activo: verde
      this.background.setFillStyle(0x00ff00, 0.8);
      this.background.setStrokeStyle(3, 0x00cc00, 1);
      this.icon.setColor('#000000');
      this.icon.setText('✎'); // Lápiz
    } else {
      // Modo inactivo: gris
      this.background.setFillStyle(0x444444, 0.8);
      this.background.setStrokeStyle(3, 0x888888, 1);
      this.icon.setColor('#ffffff');
      this.icon.setText('✎'); // Lápiz
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
    this.background.destroy();
    this.icon.destroy();
    this.button.destroy();
  }
}

