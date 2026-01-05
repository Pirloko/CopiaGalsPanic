import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';

/**
 * Escena del menú principal
 */
export class MenuScene extends Phaser.Scene {
  private startButton!: Phaser.GameObjects.Text;
  private isMobile: boolean = false;

  constructor() {
    super({ key: 'MenuScene' });
  }

  create(): void {
    const centerX = GAME_CONFIG.WIDTH / 2;
    const centerY = GAME_CONFIG.HEIGHT / 2;

    // Detectar si es móvil
    this.isMobile = (globalThis as any).__GAME_IS_MOBILE__ || false;

    // Fondo
    this.add.rectangle(centerX, centerY, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT, 0x1a1a2e);

    // Título
    this.add.text(centerX, centerY - 150, 'GALS PANIC', {
      fontSize: '64px',
      fontFamily: 'Arial',
      color: '#ff00ff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Botón de inicio (texto adaptado para móvil)
    const startText = this.isMobile 
      ? 'TOCA para comenzar' 
      : 'Presiona ESPACIO para comenzar';
    
    this.startButton = this.add.text(centerX, centerY, startText, {
      fontSize: '28px',
      fontFamily: 'Arial',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Efecto de parpadeo en el botón
    this.tweens.add({
      targets: this.startButton,
      alpha: 0.5,
      duration: 800,
      yoyo: true,
      repeat: -1,
    });

    // Instrucciones (adaptadas para móvil)
    const instructions = this.isMobile
      ? 'Joystick: esquina inferior izquierda\nToca y arrastra para dibujar polígonos\nAtrapa enemigos dentro de los polígonos'
      : 'Usa las FLECHAS para moverte\nCLICK y ARRASTRA para dibujar polígonos\nAtrapa enemigos dentro de los polígonos';

    this.add.text(
      centerX,
      centerY + 100,
      instructions,
      {
        fontSize: '18px',
        fontFamily: 'Arial',
        color: '#aaaaaa',
        align: 'center',
      }
    ).setOrigin(0.5);

    // Hacer toda la pantalla clickeable/touchable
    const fullScreenZone = this.add.rectangle(centerX, centerY, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT, 0x000000, 0);
    fullScreenZone.setInteractive({ useHandCursor: true });
    fullScreenZone.on('pointerdown', () => {
      this.startGame();
    });

    // Controles de teclado (solo si no es móvil)
    if (!this.isMobile && this.input.keyboard) {
      const spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
      spaceKey.on('down', () => {
        this.startGame();
      });
    }

    // También permitir click/touch en el botón
    this.startButton.setInteractive({ useHandCursor: true });
    this.startButton.on('pointerdown', () => {
      this.startGame();
    });
  }

  /**
   * Inicia el juego
   */
  private startGame(): void {
    this.scene.start('GameScene');
  }
}
