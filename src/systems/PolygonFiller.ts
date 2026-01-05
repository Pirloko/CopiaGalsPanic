import Phaser from 'phaser';
import { Point, Geometry } from '../utils/geometry';
import { GAME_CONFIG, POLYGON_FILLER_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';

/**
 * Sistema de rellenado de polígonos
 * Utiliza algoritmo scanline para rellenar polígonos y calcular áreas reveladas
 */
export class PolygonFiller {
  private scene: Phaser.Scene;
  private fillGraphics!: Phaser.GameObjects.Graphics;
  private revealedData: Uint8Array;
  private polygons: Point[][] = [];
  private totalRevealedArea: number = 0;
  private totalGameArea: number;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.totalGameArea = GAME_CONFIG.GAME_AREA_WIDTH * GAME_CONFIG.GAME_AREA_HEIGHT;
    
    // Crear array para almacenar el estado de cada pixel (0 = no revelado, 1 = revelado)
    this.revealedData = new Uint8Array(
      GAME_CONFIG.GAME_AREA_WIDTH * GAME_CONFIG.GAME_AREA_HEIGHT
    );

    this.setupGraphics();
  }

  /**
   * Configura los objetos Graphics para el rellenado
   */
  private setupGraphics(): void {
    this.fillGraphics = this.scene.add.graphics();
    this.fillGraphics.setDepth(0); // Detrás de las líneas pero encima del fondo
  }

  /**
   * Rellena un polígono usando algoritmo scanline
   */
  public fillPolygon(vertices: Point[]): void {
    if (vertices.length < 3) return;

    // Calcular el área del polígono antes de rellenar
    const polygonArea = Geometry.polygonArea(vertices);

    // Verificar si este polígono está anidado dentro de otro
    const isNested = this.isPolygonNested(vertices);
    
    if (isNested) {
      // Si está anidado, no contar su área (ya está contada)
      // Pero sí rellenarlo visualmente
      this.scanlineFill(vertices);
      return;
    }

    // Rellenar el polígono
    this.scanlineFill(vertices);

    // Almacenar el polígono
    this.polygons.push([...vertices]);

    // Actualizar área total revelada (solo si no está anidado)
    this.totalRevealedArea += polygonArea;

    // Calcular porcentaje revelado
    const percentage = (this.totalRevealedArea / this.totalGameArea) * 100;

    // Emitir evento con datos del polígono
    this.scene.events.emit(GameEvents.POLYGON_VALIDATED, {
      vertices: vertices,
      area: polygonArea,
      totalArea: this.totalRevealedArea,
      percentage: percentage,
    });
  }

  /**
   * Algoritmo scanline para rellenar polígonos
   * Usa una versión simplificada con pointInPolygon para robustez
   */
  private scanlineFill(vertices: Point[]): void {
    // Encontrar bounding box
    let minX = Infinity;
    let maxX = -Infinity;
    let minY = Infinity;
    let maxY = -Infinity;

    for (const v of vertices) {
      minX = Math.min(minX, Math.floor(v.x));
      maxX = Math.max(maxX, Math.ceil(v.x));
      minY = Math.min(minY, Math.floor(v.y));
      maxY = Math.max(maxY, Math.ceil(v.y));
    }

    minX = Math.max(0, minX);
    maxX = Math.min(GAME_CONFIG.GAME_AREA_WIDTH - 1, maxX);
    minY = Math.max(0, minY);
    maxY = Math.min(GAME_CONFIG.GAME_AREA_HEIGHT - 1, maxY);

    // Rellenar usando Graphics en bloques para mejor rendimiento
    this.fillGraphics.fillStyle(POLYGON_FILLER_CONFIG.REVEAL_COLOR, POLYGON_FILLER_CONFIG.FILL_ALPHA);

    // Rellenar scanline por scanline (optimizado)
    for (let y = minY; y <= maxY; y++) {
      let startX = -1;
      
      for (let x = minX; x <= maxX; x++) {
        const point: Point = { x, y };
        const isInside = Geometry.pointInPolygon(point, vertices);
        const index = y * GAME_CONFIG.GAME_AREA_WIDTH + x;
        const alreadyRevealed = this.revealedData[index] === 1;

        if (isInside && !alreadyRevealed) {
          if (startX === -1) {
            startX = x;
          }
          this.revealedData[index] = 1;
        } else {
          if (startX !== -1) {
            // Rellenar desde startX hasta x-1
            this.fillGraphics.fillRect(startX, y, x - startX, 1);
            startX = -1;
          }
        }
      }
      
      // Rellenar si la línea termina dentro del polígono
      if (startX !== -1) {
        this.fillGraphics.fillRect(startX, y, maxX - startX + 1, 1);
      }
    }
  }

  /**
   * Verifica si un polígono está anidado dentro de otro polígono existente
   */
  private isPolygonNested(vertices: Point[]): boolean {
    if (this.polygons.length === 0) return false;

    // Verificar si el centroide del nuevo polígono está dentro de algún polígono existente
    const centroid = this.getCentroid(vertices);

    for (const existingPolygon of this.polygons) {
      if (Geometry.pointInPolygon(centroid, existingPolygon)) {
        return true;
      }
    }

    return false;
  }

  /**
   * Calcula el centroide de un polígono
   */
  private getCentroid(vertices: Point[]): Point {
    let sumX = 0;
    let sumY = 0;

    for (const v of vertices) {
      sumX += v.x;
      sumY += v.y;
    }

    return {
      x: sumX / vertices.length,
      y: sumY / vertices.length,
    };
  }

  /**
   * Obtiene el porcentaje del área revelada
   */
  public getRevealedPercentage(): number {
    return (this.totalRevealedArea / this.totalGameArea) * 100;
  }

  /**
   * Obtiene el área total revelada
   */
  public getRevealedArea(): number {
    return this.totalRevealedArea;
  }

  /**
   * Obtiene todos los polígonos cerrados
   */
  public getPolygons(): Point[][] {
    return this.polygons.map(poly => [...poly]); // Retorna copias
  }

  /**
   * Resetea el sistema (para nuevos niveles)
   */
  public reset(): void {
    this.polygons = [];
    this.totalRevealedArea = 0;
    this.fillGraphics.clear();
    this.revealedData.fill(0);
  }

  /**
   * Limpia recursos
   */
  public destroy(): void {
    this.fillGraphics.destroy();
  }
}