import Phaser from 'phaser';
import { GAME_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';

/**
 * Sistema de HUD (Heads-Up Display)
 * Muestra información del juego en tiempo real
 */
export class HUD {
  private scene: Phaser.Scene;
  private container!: Phaser.GameObjects.Container;
  
  // Textos
  private timeText!: Phaser.GameObjects.Text;
  private levelText!: Phaser.GameObjects.Text;
  private scoreText!: Phaser.GameObjects.Text;
  private livesText!: Phaser.GameObjects.Text;
  private percentageText!: Phaser.GameObjects.Text;
  
  // Valores actuales
  private currentTime: string = '00:00';
  private currentLevel: number = 1;
  private currentScore: number = 0;
  private currentLives: number = GAME_CONFIG.INITIAL_LIVES;
  private currentPercentage: number = 0;
  private requiredPercentage: number = 75;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.create();
    this.setupEvents();
  }

  /**
   * Crea los elementos visuales del HUD
   */
  private create(): void {
    const x = GAME_CONFIG.GAME_AREA_WIDTH + GAME_CONFIG.HUD_WIDTH / 2;
    const startY = 50;
    const spacing = 80;

    // Contenedor para organizar elementos
    this.container = this.scene.add.container(x, 0);
    this.container.setDepth(100);

    // Título
    const title = this.scene.add.text(0, startY, 'GALS PANIC', {
      fontSize: '18px',
      fontStyle: 'bold',
      color: '#ffffff',
      align: 'center',
    });
    title.setOrigin(0.5);

    // Tiempo
    const timeLabel = this.scene.add.text(0, startY + spacing, 'TIEMPO', {
      fontSize: '12px',
      color: '#aaaaaa',
      align: 'center',
    });
    timeLabel.setOrigin(0.5);

    this.timeText = this.scene.add.text(0, startY + spacing + 20, '00:00', {
      fontSize: '20px',
      fontStyle: 'bold',
      color: '#00ff00',
      align: 'center',
    });
    this.timeText.setOrigin(0.5);

    // Nivel
    const levelLabel = this.scene.add.text(0, startY + spacing * 2, 'NIVEL', {
      fontSize: '12px',
      color: '#aaaaaa',
      align: 'center',
    });
    levelLabel.setOrigin(0.5);

    this.levelText = this.scene.add.text(0, startY + spacing * 2 + 20, '1', {
      fontSize: '24px',
      fontStyle: 'bold',
      color: '#ffff00',
      align: 'center',
    });
    this.levelText.setOrigin(0.5);

    // Puntaje
    const scoreLabel = this.scene.add.text(0, startY + spacing * 3, 'PUNTAJE', {
      fontSize: '12px',
      color: '#aaaaaa',
      align: 'center',
    });
    scoreLabel.setOrigin(0.5);

    this.scoreText = this.scene.add.text(0, startY + spacing * 3 + 20, '0', {
      fontSize: '16px',
      fontStyle: 'bold',
      color: '#ffffff',
      align: 'center',
    });
    this.scoreText.setOrigin(0.5);

    // Vidas
    const livesLabel = this.scene.add.text(0, startY + spacing * 4, 'VIDAS', {
      fontSize: '12px',
      color: '#aaaaaa',
      align: 'center',
    });
    livesLabel.setOrigin(0.5);

    this.livesText = this.scene.add.text(0, startY + spacing * 4 + 20, '❤️❤️❤️', {
      fontSize: '20px',
      align: 'center',
    });
    this.livesText.setOrigin(0.5);

    // Porcentaje
    const percentageLabel = this.scene.add.text(0, startY + spacing * 5, 'REVELADO', {
      fontSize: '12px',
      color: '#aaaaaa',
      align: 'center',
    });
    percentageLabel.setOrigin(0.5);

    this.percentageText = this.scene.add.text(0, startY + spacing * 5 + 20, '0% / 75%', {
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#00ffff',
      align: 'center',
    });
    this.percentageText.setOrigin(0.5);

    // Añadir todos los elementos al contenedor
    this.container.add([
      title,
      timeLabel,
      this.timeText,
      levelLabel,
      this.levelText,
      scoreLabel,
      this.scoreText,
      livesLabel,
      this.livesText,
      percentageLabel,
      this.percentageText,
    ]);
  }

  /**
   * Configura los listeners de eventos
   */
  private setupEvents(): void {
    // Tiempo
    this.scene.events.on(GameEvents.TIME_UPDATED, (data: { formatted: string }) => {
      this.currentTime = data.formatted;
      this.updateTimeText();
    });

    // Nivel (se actualiza cuando cambia)
    // Esto se maneja mediante métodos públicos

    // Puntaje
    this.scene.events.on(GameEvents.SCORE_UPDATED, (data: { score: number }) => {
      this.currentScore = data.score;
      this.updateScoreText();
    });

    // Vidas
    this.scene.events.on(GameEvents.LIVES_UPDATED, (data: { lives: number }) => {
      this.currentLives = data.lives;
      this.updateLivesText();
    });

    // Porcentaje (se actualiza manualmente desde GameScene)
  }

  /**
   * Actualiza el texto del tiempo
   */
  private updateTimeText(): void {
    this.timeText.setText(this.currentTime);
    
    // Cambiar color si el tiempo es bajo (menos de 30 segundos)
    const seconds = parseInt(this.currentTime.split(':')[1]);
    const minutes = parseInt(this.currentTime.split(':')[0]);
    const totalSeconds = minutes * 60 + seconds;
    
    if (totalSeconds <= 10) {
      this.timeText.setColor('#ff0000'); // Rojo
    } else if (totalSeconds <= 30) {
      this.timeText.setColor('#ff8800'); // Naranja
    } else {
      this.timeText.setColor('#00ff00'); // Verde
    }
  }

  /**
   * Actualiza el texto del nivel
   */
  public updateLevel(level: number): void {
    this.currentLevel = level;
    this.levelText.setText(level.toString());
  }

  /**
   * Actualiza el texto del puntaje
   */
  private updateScoreText(): void {
    this.scoreText.setText(this.currentScore.toLocaleString());
  }

  /**
   * Actualiza el texto de las vidas
   */
  private updateLivesText(): void {
    const hearts = '❤️'.repeat(Math.max(0, this.currentLives));
    this.livesText.setText(hearts || '💀');
  }

  /**
   * Actualiza el porcentaje revelado
   */
  public updatePercentage(revealed: number, required: number): void {
    this.currentPercentage = revealed;
    this.requiredPercentage = required;
    this.percentageText.setText(
      `${revealed.toFixed(1)}% / ${required.toFixed(0)}%`
    );

    // Cambiar color según progreso
    const progress = revealed / required;
    if (progress >= 1.0) {
      this.percentageText.setColor('#00ff00'); // Verde (completado)
    } else if (progress >= 0.75) {
      this.percentageText.setColor('#ffff00'); // Amarillo (casi completo)
    } else {
      this.percentageText.setColor('#00ffff'); // Cyan (normal)
    }
  }

  /**
   * Limpia recursos
   */
  public destroy(): void {
    this.container.destroy();
  }
}