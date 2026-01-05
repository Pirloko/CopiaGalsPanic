/**
 * Utilidades para detección de dispositivo
 */

/**
 * Detecta si el dispositivo es móvil
 */
export function isMobileDevice(): boolean {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  ) || (window.innerWidth <= 768);
}

/**
 * Detecta si es un dispositivo táctil
 */
export function isTouchDevice(): boolean {
  return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
}

/**
 * Obtiene el tamaño de pantalla del dispositivo
 */
export function getScreenSize(): { width: number; height: number } {
  return {
    width: window.innerWidth,
    height: window.innerHeight,
  };
}

