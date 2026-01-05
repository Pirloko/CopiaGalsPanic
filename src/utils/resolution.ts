import { GAME_CONFIG } from '../config/gameConfig';
import { isMobileDevice } from './device';

/**
 * Configuración de resolución para diferentes dispositivos
 */

/**
 * Configuración base del juego
 */
const BASE_WIDTH = GAME_CONFIG.WIDTH;
const BASE_HEIGHT = GAME_CONFIG.HEIGHT;

/**
 * Calcula las dimensiones adaptadas para el dispositivo
 */
export function getAdaptedDimensions(): {
  width: number;
  height: number;
  scale: number;
  mode: 'desktop' | 'mobile';
} {
  const isMobile = isMobileDevice();
  const screenWidth = window.innerWidth;
  const screenHeight = window.innerHeight;
  
  if (isMobile) {
    // En móviles, usar toda la pantalla
    // Ajustar para mantener aspect ratio
    const aspectRatio = BASE_WIDTH / BASE_HEIGHT;
    let width = screenWidth;
    let height = screenWidth / aspectRatio;
    
    // Si el alto es mayor que la pantalla, ajustar por alto
    if (height > screenHeight) {
      height = screenHeight;
      width = height * aspectRatio;
    }
    
    return {
      width: Math.floor(width),
      height: Math.floor(height),
      scale: width / BASE_WIDTH,
      mode: 'mobile',
    };
  } else {
    // Desktop: mantener tamaño base
    return {
      width: BASE_WIDTH,
      height: BASE_HEIGHT,
      scale: 1,
      mode: 'desktop',
    };
  }
}

