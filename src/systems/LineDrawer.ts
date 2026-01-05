import Phaser from 'phaser';
import { Geometry, Point } from '../utils/geometry';
import { LINE_DRAWER_CONFIG } from '../config/gameConfig';
import { GameEvents } from '../config/events';
import { Player } from '../entities/Player';

/**
 * Sistema de dibujo de líneas
 * Dibuja las líneas trazadas por el jugador (sigue la posición del jugador, no el mouse)
 */
export class LineDrawer {
  private scene: Phaser.Scene;
  private graphics!: Phaser.GameObjects.Graphics;
  private closeIndicatorGraphics!: Phaser.GameObjects.Graphics;
  private player?: Player;

  constructor(scene: Phaser.Scene) {
    this.scene = scene;
    this.setupGraphics();
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
   * Establece la referencia al jugador
   */
  public setPlayer(player: Player): void {
    this.player = player;
  }

  /**
   * Dibuja la línea actual del trazado del jugador
   */
  public drawTrace(): void {
    this.graphics.clear();
    this.closeIndicatorGraphics.clear();

    if (!this.player || !this.player.isTracing) {
      return;
    }

    const points = this.player.getTracePoints();

    if (points.length < 2) {
      return;
    }

    // Dibujar línea principal
    this.graphics.lineStyle(
      LINE_DRAWER_CONFIG.LINE_WIDTH,
      LINE_DRAWER_CONFIG.LINE_COLOR,
      1
    );

    this.graphics.beginPath();
    this.graphics.moveTo(points[0].x, points[0].y);

    for (let i = 1; i < points.length; i++) {
      this.graphics.lineTo(points[i].x, points[i].y);
    }

    this.graphics.strokePath();

    // Dibujar línea de predicción (verde) si hay punto de cierre cercano
    const predictionPoint = this.player.getPredictionPoint();
    if (predictionPoint && points.length >= 3) {
      const currentPos = { x: this.player.x, y: this.player.y };
      
      this.closeIndicatorGraphics.lineStyle(
        LINE_DRAWER_CONFIG.LINE_WIDTH + 1,
        LINE_DRAWER_CONFIG.CLOSE_INDICATOR_COLOR,
        0.8
      );

      this.closeIndicatorGraphics.beginPath();
      this.closeIndicatorGraphics.moveTo(currentPos.x, currentPos.y);
      this.closeIndicatorGraphics.lineTo(predictionPoint.x, predictionPoint.y);
      this.closeIndicatorGraphics.strokePath();
    }
  }

  /**
   * Procesa el trazado cuando se detiene (cuando se suelta el botón)
   */
  public processTrace(): void {
    if (!this.player) {
      return;
    }

    const points = this.player.stopTracing();

    if (points.length < 3) {
      this.clearLine();
      return;
    }

    // Validar el polígono
    if (!Geometry.isValidPolygon(points)) {
      this.clearLine();
      return;
    }

    // Verificar si el polígono está cerrado (si el último punto está cerca del primero)
    const firstPoint = points[0];
    const lastPoint = points[points.length - 1];
    const distanceToStart = Geometry.distance(lastPoint, firstPoint);

    if (distanceToStart <= LINE_DRAWER_CONFIG.CLOSE_DISTANCE_THRESHOLD) {
      // Cerrar el polígono conectando el último punto con el primero
      const closedPoints = [...points];
      closedPoints.push({ ...firstPoint });

      // Emitir evento
      const area = Geometry.polygonArea(closedPoints);
      this.scene.events.emit(GameEvents.AREA_CLOSED, {
        vertices: closedPoints,
        area: area,
      });
    } else {
      // Polígono no cerrado, limpiar
      this.clearLine();
    }
  }

  /**
   * Limpia la línea actual
   */
  public clearLine(): void {
    this.graphics.clear();
    this.closeIndicatorGraphics.clear();
  }

  /**
   * Actualización del sistema (para dibujar cada frame)
   */
  public update(_delta: number): void {
    this.drawTrace();
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
