/**
 * Utilidades geométricas
 * Funciones matemáticas para cálculos geométricos en 2D
 */

export interface Point {
  x: number;
  y: number;
}

export namespace Geometry {
  /**
   * Calcula la distancia euclidiana entre dos puntos
   */
  export function distance(p1: Point, p2: Point): number {
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  /**
   * Calcula el ángulo entre dos puntos en radianes
   * @returns Ángulo en radianes (0 a 2π)
   */
  export function angleBetween(p1: Point, p2: Point): number {
    return Math.atan2(p2.y - p1.y, p2.x - p1.x);
  }

  /**
   * Calcula la distancia más corta entre un punto y un segmento de línea
   */
  export function pointSegmentDistance(
    point: Point,
    segStart: Point,
    segEnd: Point
  ): number {
    const A = point.x - segStart.x;
    const B = point.y - segStart.y;
    const C = segEnd.x - segStart.x;
    const D = segEnd.y - segStart.y;

    const dot = A * C + B * D;
    const lenSq = C * C + D * D;
    let param = -1;

    if (lenSq !== 0) {
      param = dot / lenSq;
    }

    let xx: number, yy: number;

    if (param < 0) {
      xx = segStart.x;
      yy = segStart.y;
    } else if (param > 1) {
      xx = segEnd.x;
      yy = segEnd.y;
    } else {
      xx = segStart.x + param * C;
      yy = segStart.y + param * D;
    }

    const dx = point.x - xx;
    const dy = point.y - yy;
    return Math.sqrt(dx * dx + dy * dy);
  }

  /**
   * Detecta colisión entre una línea (segmento) y un círculo
   * @returns true si hay colisión
   */
  export function lineCircleCollision(
    lineStart: Point,
    lineEnd: Point,
    circleCenter: Point,
    circleRadius: number
  ): boolean {
    const dist = pointSegmentDistance(circleCenter, lineStart, lineEnd);
    return dist <= circleRadius;
  }

  /**
   * Calcula el área de un polígono usando la fórmula del shoelace
   * @param vertices Array de vértices del polígono (debe estar cerrado)
   * @returns Área del polígono (positiva si es counter-clockwise, negativa si es clockwise)
   */
  export function polygonArea(vertices: Point[]): number {
    if (vertices.length < 3) return 0;

    let area = 0;
    for (let i = 0; i < vertices.length; i++) {
      const j = (i + 1) % vertices.length;
      area += vertices[i].x * vertices[j].y;
      area -= vertices[j].x * vertices[i].y;
    }
    return Math.abs(area / 2);
  }

  /**
   * Determina si un punto está dentro de un polígono usando ray casting algorithm
   * @param point Punto a verificar
   * @param vertices Array de vértices del polígono
   * @returns true si el punto está dentro del polígono
   */
  export function pointInPolygon(point: Point, vertices: Point[]): boolean {
    if (vertices.length < 3) return false;

    let inside = false;
    for (let i = 0, j = vertices.length - 1; i < vertices.length; j = i++) {
      const xi = vertices[i].x,
        yi = vertices[i].y;
      const xj = vertices[j].x,
        yj = vertices[j].y;

      const intersect =
        yi > point.y !== yj > point.y &&
        point.x < ((xj - xi) * (point.y - yi)) / (yj - yi) + xi;
      if (intersect) inside = !inside;
    }

    return inside;
  }

  /**
   * Verifica si dos segmentos de línea se intersectan
   */
  function segmentsIntersect(
    p1: Point,
    p2: Point,
    p3: Point,
    p4: Point
  ): boolean {
    const d = (p2.x - p1.x) * (p4.y - p3.y) - (p2.y - p1.y) * (p4.x - p3.x);
    if (d === 0) return false;

    const t =
      ((p3.x - p1.x) * (p4.y - p3.y) - (p3.y - p1.y) * (p4.x - p3.x)) / d;
    const u =
      ((p3.x - p1.x) * (p2.y - p1.y) - (p3.y - p1.y) * (p2.x - p1.x)) / d;

    return t >= 0 && t <= 1 && u >= 0 && u <= 1;
  }

  /**
   * Valida si un polígono es válido
   * - Debe tener al menos 3 vértices
   * - No debe autointersectarse (verificación básica)
   * @param vertices Array de vértices del polígono
   * @returns true si el polígono es válido
   */
  export function isValidPolygon(vertices: Point[]): boolean {
    // Mínimo 3 vértices
    if (vertices.length < 3) return false;

    // Verificar autointersección (comparar cada segmento con los demás)
    for (let i = 0; i < vertices.length; i++) {
      const p1 = vertices[i];
      const p2 = vertices[(i + 1) % vertices.length];

      // Comparar con segmentos no adyacentes
      for (let j = i + 2; j < vertices.length; j++) {
        // Saltar el último segmento si estamos en el primero
        if (i === 0 && j === vertices.length - 1) continue;

        const p3 = vertices[j];
        const p4 = vertices[(j + 1) % vertices.length];

        if (segmentsIntersect(p1, p2, p3, p4)) {
          return false;
        }
      }
    }

    return true;
  }

  /**
   * Calcula el punto más cercano a un punto dado en un segmento de línea
   */
  export function closestPointOnSegment(
    point: Point,
    segStart: Point,
    segEnd: Point
  ): Point {
    const A = point.x - segStart.x;
    const B = point.y - segStart.y;
    const C = segEnd.x - segStart.x;
    const D = segEnd.y - segStart.y;

    const dot = A * C + B * D;
    const lenSq = C * C + D * D;
    let param = -1;

    if (lenSq !== 0) {
      param = dot / lenSq;
    }

    if (param < 0) {
      return { x: segStart.x, y: segStart.y };
    } else if (param > 1) {
      return { x: segEnd.x, y: segEnd.y };
    } else {
      return {
        x: segStart.x + param * C,
        y: segStart.y + param * D,
      };
    }
  }
}