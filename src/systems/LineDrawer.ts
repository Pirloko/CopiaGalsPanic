import Phaser from 'phaser';
import { Geometry, Point } from '../utils/geometry';
import { LINE_DRAWER_CONFIG } from '../config/gameConfig';
import { GAME_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';

/**
 * Sistema de dibujo de líneas
 * Captura puntos del mouse/touch y dibuja líneas en tiempo real
 */
export class LineDrawer {
  private scene: Phaser.Scene;
  private graphics!: Phaser.GameObjects.Graphics;
  private points: Point[] = [];
  private isDrawing: boolean = false;
  private closeIndicatorGraphics!: Phaser.GameObjects.Graphics;
  private isActive: boolean = true;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.setupGraphics();
    this.setupInput();
  }

  /**
   * Configura los objetos Graphics para dibujar
   */
  private setupGraphics(): void {
    // Graphics para la línea principal
    this.graphics = this.scene.add.graphics();
    this.graphics.setDepth(1);

    // Graphics para el indicador de cierre (línea verde)
    this.closeIndicatorGraphics = this.scene.add.graphics();
    this.closeIndicatorGraphics.setDepth(2);
  }

  /**
   * Configura los eventos de entrada (mouse y touch)
   */
  private setupInput(): void {
    // Mouse
    this.scene.input.on('pointerdown', this.startDrawing, this);
    this.scene.input.on('pointermove', this.updateDrawing, this);
    this.scene.input.on('pointerup', this.stopDrawing, this);

    // Touch
    this.scene.input.on('pointerdown', this.startDrawing, this);
    this.scene.input.on('pointermove', this.updateDrawing, this);
    this.scene.input.on('pointerup', this.stopDrawing, this);
  }

  /**
   * Inicia el dibujo de una nueva línea
   */
  private startDrawing(pointer: Phaser.Input.Pointer): void {
    if (!this.isActive) return;

    const worldPoint = this.getWorldPoint(pointer);
    if (!this.isPointInGameArea(worldPoint)) return;

    this.isDrawing = true;
    this.points = [worldPoint];
    this.clearLine();
  }

  /**
   * Actualiza el dibujo mientras se mueve el mouse/touch
   */
  private updateDrawing(pointer: Phaser.Input.Pointer): void {
    if (!this.isDrawing || !this.isActive) return;

    const worldPoint = this.getWorldPoint(pointer);

    // Verificar que el punto está en el área de juego
    if (!this.isPointInGameArea(worldPoint)) return;

    // Verificar distancia mínima para evitar acumulación excesiva de puntos
    if (this.points.length > 0) {
      const lastPoint = this.points[this.points.length - 1];
      const dist = Geometry.distance(lastPoint, worldPoint);

      if (dist < LINE_DRAWER_CONFIG.MIN_POINT_DISTANCE) {
        return; // No añadir punto si está muy cerca
      }
    }

    this.points.push(worldPoint);
    this.drawLine();

    // Verificar si estamos cerca del punto inicial (cierre de polígono)
    this.checkPolygonClose(worldPoint);
  }

  /**
   * Detiene el dibujo y valida el polígono si está cerrado
   */
  private stopDrawing(): void {
    if (!this.isDrawing) return;

    this.isDrawing = false;
    this.closeIndicatorGraphics.clear();

    // Si hay suficientes puntos, intentar validar y cerrar
    if (this.points.length >= 3) {
      // Validar el polígono
      if (Geometry.isValidPolygon(this.points)) {
        this.onPolygonClosed(this.points);
      } else {
        // Polígono inválido, resetear
        this.clearLine();
      }
    } else {
      // No hay suficientes puntos, limpiar
      this.clearLine();
    }
  }

  /**
   * Dibuja la línea actual
   */
  private drawLine(): void {
    this.graphics.clear();
    
    if (this.points.length < 2) return;

    this.graphics.lineStyle(
      LINE_DRAWER_CONFIG.LINE_WIDTH,
      LINE_DRAWER_CONFIG.LINE_COLOR,
      1
    );

    this.graphics.beginPath();
    this.graphics.moveTo(this.points[0].x, this.points[0].y);

    for (let i = 1; i < this.points.length; i++) {
      this.graphics.lineTo(this.points[i].x, this.points[i].y);
    }

    this.graphics.strokePath();
  }

  /**
   * Verifica si estamos cerca del punto inicial y muestra indicador
   */
  private checkPolygonClose(currentPoint: Point): void {
    if (this.points.length < 3) {
      this.closeIndicatorGraphics.clear();
      return;
    }

    const firstPoint = this.points[0];
    const distanceToStart = Geometry.distance(currentPoint, firstPoint);

    if (distanceToStart <= LINE_DRAWER_CONFIG.CLOSE_DISTANCE_THRESHOLD) {
      // Dibujar línea verde indicando que se puede cerrar
      this.closeIndicatorGraphics.clear();
      this.closeIndicatorGraphics.lineStyle(
        LINE_DRAWER_CONFIG.LINE_WIDTH + 1,
        LINE_DRAWER_CONFIG.CLOSE_INDICATOR_COLOR,
        0.8
      );
      this.closeIndicatorGraphics.beginPath();
      this.closeIndicatorGraphics.moveTo(
        this.points[this.points.length - 1].x,
        this.points[this.points.length - 1].y
      );
      this.closeIndicatorGraphics.lineTo(firstPoint.x, firstPoint.y);
      this.closeIndicatorGraphics.strokePath();
    } else {
      this.closeIndicatorGraphics.clear();
    }
  }

  /**
   * Convierte las coordenadas del pointer a coordenadas del mundo del juego
   */
  private getWorldPoint(pointer: Phaser.Input.Pointer): Point {
    // En móviles con Scale.FIT, necesitamos convertir coordenadas de pantalla a mundo
    // Usar la cámara principal para convertir coordenadas
    const camera = this.scene.cameras.main;
    const worldX = camera.getWorldPoint(pointer.x, pointer.y).x;
    const worldY = camera.getWorldPoint(pointer.x, pointer.y).y;
    
    return {
      x: worldX,
      y: worldY,
    };
  }

  /**
   * Verifica si un punto está dentro del área de juego
   */
  private isPointInGameArea(point: Point): boolean {
    return (
      point.x >= 0 &&
      point.x <= GAME_CONFIG.GAME_AREA_WIDTH &&
      point.y >= 0 &&
      point.y <= GAME_CONFIG.GAME_AREA_HEIGHT
    );
  }

  /**
   * Se llama cuando se cierra un polígono válido
   */
  private onPolygonClosed(vertices: Point[]): void {
    const area = Geometry.polygonArea(vertices);

    // Emitir evento
    this.scene.events.emit(GameEvents.AREA_CLOSED, {
      vertices: vertices,
      area: area,
    });

    // Mantener la línea dibujada (no limpiar)
    // El PolygonFiller se encargará del rellenado
  }

  /**
   * Limpia la línea actual
   */
  public clearLine(): void {
    this.points = [];
    this.graphics.clear();
    this.closeIndicatorGraphics.clear();
    this.isDrawing = false;
  }

  /**
   * Obtiene los puntos actuales de la línea
   */
  public getPoints(): Point[] {
    return [...this.points];
  }

  /**
   * Verifica si está dibujando actualmente
   */
  public getIsDrawing(): boolean {
    return this.isDrawing;
  }

  /**
   * Activa o desactiva el sistema de dibujo
   */
  public setActive(active: boolean): void {
    this.isActive = active;
    if (!active) {
      this.clearLine();
    }
  }

  /**
   * Actualización del sistema (para lógica adicional si es necesaria)
   */
  public update(_delta: number): void {
    // Por ahora no hay lógica adicional, pero se deja preparado
  }

  /**
   * Limpia recursos
   */
  public destroy(): void {
    this.clearLine();
    this.graphics.destroy();
    this.closeIndicatorGraphics.destroy();
  }
}