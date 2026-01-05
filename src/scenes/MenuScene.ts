import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';

/**
 * Escena del menú principal
 */
export class MenuScene extends Phaser.Scene {
  private titleText!: Phaser.GameObjects.Text;
  private startButton!: Phaser.GameObjects.Text;
  private instructionsText!: Phaser.GameObjects.Text;

  constructor() {
    super({ key: 'MenuScene' });
  }

  create(): void {
    const centerX = GAME_CONFIG.WIDTH / 2;
    const centerY = GAME_CONFIG.HEIGHT / 2;

    // Fondo
    this.add.rectangle(centerX, centerY, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT, 0x1a1a2e);

    // Título
    this.titleText = this.add.text(centerX, centerY - 150, 'GALS PANIC', {
      fontSize: '64px',
      fontFamily: 'Arial',
      color: '#ff00ff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Botón de inicio
    this.startButton = this.add.text(centerX, centerY, 'Presiona ESPACIO para comenzar', {
      fontSize: '24px',
      fontFamily: 'Arial',
      color: '#ffffff',
    }).setOrigin(0.5);

    // Efecto de parpadeo en el botón
    this.tweens.add({
      targets: this.startButton,
      alpha: 0.5,
      duration: 800,
      yoyo: true,
      repeat: -1,
    });

    // Instrucciones
    this.instructionsText = this.add.text(
      centerX,
      centerY + 100,
      'Usa las FLECHAS para moverte\nCLICK y ARRASTRA para dibujar polígonos\nAtrapa enemigos dentro de los polígonos',
      {
        fontSize: '18px',
        fontFamily: 'Arial',
        color: '#aaaaaa',
        align: 'center',
      }
    ).setOrigin(0.5);

    // Controles
    const spaceKey = this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    spaceKey.on('down', () => {
      this.scene.start('GameScene');
    });

    // También permitir click en el botón
    this.startButton.setInteractive({ useHandCursor: true });
    this.startButton.on('pointerdown', () => {
      this.scene.start('GameScene');
    });
  }
}
