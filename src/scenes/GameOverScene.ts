import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';

interface GameOverData {
  score?: number;
  level?: number;
  reason?: string;
}

/**
 * Escena de Game Over
 */
export class GameOverScene extends Phaser.Scene {
  private gameOverText!: Phaser.GameObjects.Text;
  private restartButton!: Phaser.GameObjects.Text;
  private menuButton!: Phaser.GameObjects.Text;

  constructor() {
    super({ key: 'GameOverScene' });
  }

  init(data: GameOverData): void {
    // Recibir datos del juego
    this.registry.set('finalScore', data.score || 0);
    this.registry.set('finalLevel', data.level || 1);
    this.registry.set('gameOverReason', data.reason || 'unknown');
  }

  create(): void {
    const centerX = GAME_CONFIG.WIDTH / 2;
    const centerY = GAME_CONFIG.HEIGHT / 2;

    const finalScore = this.registry.get('finalScore') as number;
    const finalLevel = this.registry.get('finalLevel') as number;
    const reason = this.registry.get('gameOverReason') as string;

    // Fondo
    this.add.rectangle(centerX, centerY, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT, 0x2a1a1a);

    // Título Game Over
    this.gameOverText = this.add.text(centerX, centerY - 150, 'GAME OVER', {
      fontSize: '64px',
      fontFamily: 'Arial',
      color: '#ff0000',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Razón del game over
    let reasonText = '';
    switch (reason) {
      case 'lives':
        reasonText = 'Te quedaste sin vidas';
        break;
      case 'time':
        reasonText = 'Se acabó el tiempo';
        break;
      case 'completed':
        reasonText = '¡Juego completado!';
        this.gameOverText.setText('¡VICTORIA!');
        this.gameOverText.setColor('#00ff00');
        break;
      default:
        reasonText = 'Fin del juego';
    }

    this.add.text(centerX, centerY - 80, reasonText, {
      fontSize: '24px',
      fontFamily: 'Arial',
      color: '#ffffff',
    }).setOrigin(0.5);

    // Nivel alcanzado
    this.add.text(centerX, centerY - 20, `Nivel alcanzado: ${finalLevel}`, {
      fontSize: '20px',
      fontFamily: 'Arial',
      color: '#aaaaaa',
    }).setOrigin(0.5);

    // Puntaje final
    this.add.text(centerX, centerY + 30, `Puntaje final: ${finalScore.toLocaleString()}`, {
      fontSize: '28px',
      fontFamily: 'Arial',
      color: '#ffff00',
      fontStyle: 'bold',
    }).setOrigin(0.5);

    // Detectar si es móvil
    const isMobile = (globalThis as any).__GAME_IS_MOBILE__ || false;

    // Botón reiniciar (texto adaptado para móvil)
    const restartText = isMobile ? 'Toca para reiniciar' : 'Presiona R para reiniciar';
    this.restartButton = this.add.text(centerX, centerY + 120, restartText, {
      fontSize: '24px',
      fontFamily: 'Arial',
      color: '#00ffff',
      fontStyle: 'bold',
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    // Botón menú (texto adaptado para móvil)
    const menuText = isMobile ? 'Toca para menú' : 'Presiona M para menú';
    this.menuButton = this.add.text(centerX, centerY + 160, menuText, {
      fontSize: '24px',
      fontFamily: 'Arial',
      color: '#ffffff',
      fontStyle: 'bold',
    }).setOrigin(0.5).setInteractive({ useHandCursor: true });

    // Controles de teclado (si está disponible)
    if (this.input.keyboard) {
      const rKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.R);
      rKey.on('down', () => {
        this.scene.start('GameScene');
      });

      const mKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.M);
      mKey.on('down', () => {
        this.scene.start('MenuScene');
      });
    }

    // Click/touch en botones (funciona en móviles)
    this.restartButton.on('pointerdown', () => {
      this.scene.start('GameScene');
    });

    this.menuButton.on('pointerdown', () => {
      this.scene.start('MenuScene');
    });
  }
}
