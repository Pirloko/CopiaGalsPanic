import Phaser from 'phaser';
import { MenuScene } from './scenes/MenuScene';
import { GameScene } from './scenes/GameScene';
import { GameOverScene } from './scenes/GameOverScene';
import { LevelCompleteScene } from './scenes/LevelCompleteScene';
import { GAME_CONFIG } from './config/gameConfig';

/**
 * Punto de entrada principal del juego
 */
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: GAME_CONFIG.WIDTH,
  height: GAME_CONFIG.HEIGHT,
  parent: 'game-container',
  backgroundColor: '#000000',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: GAME_CONFIG.GRAVITY },
      debug: false
    }
  },
  scene: [MenuScene, GameScene, LevelCompleteScene, GameOverScene],
  fps: {
    target: GAME_CONFIG.TARGET_FPS,
    forceSetTimeOut: true
  }
};

new Phaser.Game(config);
