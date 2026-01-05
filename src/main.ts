import Phaser from 'phaser';
import { MenuScene } from './scenes/MenuScene';
import { GameScene } from './scenes/GameScene';
import { GameOverScene } from './scenes/GameOverScene';
import { LevelCompleteScene } from './scenes/LevelCompleteScene';
import { GAME_CONFIG } from './config/gameConfig';
import { isMobileDevice, isTouchDevice } from './utils/device';

/**
 * Punto de entrada principal del juego
 * Configuración responsive para móviles y desktop
 */
const isMobile = isMobileDevice();
const isTouch = isTouchDevice();

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: GAME_CONFIG.WIDTH,
  height: GAME_CONFIG.HEIGHT,
  parent: 'game-container',
  backgroundColor: '#000000',
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH,
    width: GAME_CONFIG.WIDTH,
    height: GAME_CONFIG.HEIGHT,
  },
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: GAME_CONFIG.GRAVITY },
      debug: false
    }
  },
  scene: [MenuScene, GameScene, LevelCompleteScene, GameOverScene],
  fps: {
    target: GAME_CONFIG.TARGET_FPS,
    forceSetTimeOut: true
  },
  input: {
    activePointers: 3, // Permitir múltiples toques
  },
};

// Almacenar información de dispositivo para las scenes
(globalThis as any).__GAME_IS_MOBILE__ = isMobile;
(globalThis as any).__GAME_IS_TOUCH__ = isTouch;

new Phaser.Game(config);
