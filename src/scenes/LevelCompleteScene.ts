import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';

interface LevelCompleteData {
  level: number;
  score: number;
  nextLevel?: number;
}

/**
 * Escena de transición entre niveles
 */
export class LevelCompleteScene extends Phaser.Scene {
  private levelCompleteText!: Phaser.GameObjects.Text;
  private scoreText!: Phaser.GameObjects.Text;
  private nextLevelText!: Phaser.GameObjects.Text;
  private continueText!: Phaser.GameObjects.Text;
  private fadeInComplete: boolean = false;

  constructor() {
    super({ key: 'LevelCompleteScene' });
  }

  init(data: LevelCompleteData): void {
    this.registry.set('completedLevel', data.level);
    this.registry.set('currentScore', data.score);
    this.registry.set('nextLevel', data.nextLevel);
  }

  create(): void {
    const centerX = GAME_CONFIG.WIDTH / 2;
    const centerY = GAME_CONFIG.HEIGHT / 2;

    const completedLevel = this.registry.get('completedLevel') as number;
    const currentScore = this.registry.get('currentScore') as number;
    const nextLevel = this.registry.get('nextLevel') as number;

    // Fondo (inicio con alpha 0 para fade in)
    const bg = this.add.rectangle(centerX, centerY, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT, 0x1a2a1a);
    bg.setAlpha(0);

    // Título
    this.levelCompleteText = this.add.text(centerX, centerY - 120, `Nivel ${completedLevel} Completado!`, {
      fontSize: '48px',
      fontFamily: 'Arial',
      color: '#00ff00',
      fontStyle: 'bold',
    }).setOrigin(0.5).setAlpha(0);

    // Puntaje
    this.scoreText = this.add.text(centerX, centerY - 40, `Puntaje: ${currentScore.toLocaleString()}`, {
      fontSize: '28px',
      fontFamily: 'Arial',
      color: '#ffff00',
    }).setOrigin(0.5).setAlpha(0);

    // Siguiente nivel
    if (nextLevel && nextLevel <= GAME_CONFIG.MAX_LEVELS) {
      this.nextLevelText = this.add.text(centerX, centerY + 40, `Siguiente nivel: ${nextLevel}`, {
        fontSize: '24px',
        fontFamily: 'Arial',
        color: '#ffffff',
      }).setOrigin(0.5).setAlpha(0);
    } else {
      this.nextLevelText = this.add.text(centerX, centerY + 40, '¡Juego completado!', {
        fontSize: '24px',
        fontFamily: 'Arial',
        color: '#00ffff',
      }).setOrigin(0.5).setAlpha(0);
    }

    // Texto para continuar
    this.continueText = this.add.text(centerX, centerY + 120, 'Presiona ESPACIO para continuar', {
      fontSize: '20px',
      fontFamily: 'Arial',
      color: '#aaaaaa',
    }).setOrigin(0.5).setAlpha(0);

    // Animación de fade in
    this.tweens.add({
      targets: bg,
      alpha: 1,
      duration: 500,
    });

    this.tweens.add({
      targets: [this.levelCompleteText, this.scoreText, this.nextLevelText],
      alpha: 1,
      duration: 800,
      delay: 200,
      onComplete: () => {
        this.fadeInComplete = true;
        // Mostrar texto de continuar con parpadeo
        this.tweens.add({
          targets: this.continueText,
          alpha: 1,
          duration: 400,
        });
        this.tweens.add({
          targets: this.continueText,
          alpha: 0.5,
          duration: 800,
          yoyo: true,
          repeat: -1,
        });
      },
    });

    // Controles (solo después del fade in)
    const spaceKey = this.input.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);
    spaceKey.on('down', () => {
      if (this.fadeInComplete) {
        this.continueToNext();
      }
    });

    // Click para continuar
    this.input.on('pointerdown', () => {
      if (this.fadeInComplete) {
        this.continueToNext();
      }
    });

    // Auto-continuar después de 3 segundos
    this.time.delayedCall(3000, () => {
      if (this.fadeInComplete) {
        this.continueToNext();
      }
    });
  }

  private continueToNext(): void {
    const nextLevel = this.registry.get('nextLevel') as number;
    
    if (nextLevel && nextLevel <= GAME_CONFIG.MAX_LEVELS) {
      // Continuar al siguiente nivel
      this.scene.start('GameScene', { level: nextLevel });
    } else {
      // Juego completado, ir a Game Over con razón "completed"
      this.scene.start('GameOverScene', {
        score: this.registry.get('currentScore'),
        level: GAME_CONFIG.MAX_LEVELS,
        reason: 'completed',
      });
    }
  }
}
