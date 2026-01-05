import Phaser from 'phaser';

/**
 * Sistema de gestión de audio
 * Maneja efectos de sonido y música
 * Nota: En esta implementación básica, los sonidos son opcionales
 * ya que no tenemos archivos de audio. El sistema está preparado
 * para cuando se añadan recursos de audio.
 */
export class AudioManager {
  private sounds: Map<string, Phaser.Sound.BaseSound> = new Map();
  private music?: Phaser.Sound.BaseSound;
  private volume: number = 0.5;
  private musicVolume: number = 0.3;
  private enabled: boolean = true;

  constructor(_scene: Phaser.Scene) {
    // Por ahora, AudioManager está preparado pero no carga sonidos
    // ya que no tenemos archivos de audio en esta fase
    // En FASE 9 se pueden añadir sonidos reales
  }

  /**
   * Pre carga sonidos (llamar en el preload de la scene)
   */
  public preload(): void {
    // TODO: Cuando se añadan archivos de audio, cargar aquí
    // Ejemplo:
    // this.scene.load.audio('hit', 'assets/sounds/hit.wav');
    // this.scene.load.audio('powerup', 'assets/sounds/powerup.wav');
    // this.scene.load.audio('victory', 'assets/sounds/victory.wav');
    // this.scene.load.audio('explosion', 'assets/sounds/explosion.wav');
    // this.scene.load.audio('background_music', 'assets/sounds/background.mp3');
  }

  /**
   * Inicializa los sonidos (llamar en create de la scene)
   */
  public init(): void {
    // TODO: Cuando se añadan archivos de audio, crear aquí
    // Ejemplo:
    // this.sounds.set('hit', this.scene.sound.add('hit', { volume: this.volume }));
    // this.sounds.set('powerup', this.scene.sound.add('powerup', { volume: this.volume }));
    // this.sounds.set('victory', this.scene.sound.add('victory', { volume: this.volume }));
    // this.sounds.set('explosion', this.scene.sound.add('explosion', { volume: this.volume }));
    // this.music = this.scene.sound.add('background_music', { volume: this.musicVolume, loop: true });
  }

  /**
   * Reproduce un efecto de sonido
   */
  public playSound(_key: string): void {
    if (!this.enabled) return;

    const sound = this.sounds.get(_key);
    if (sound) {
      (sound as Phaser.Sound.BaseSound).play();
    }
    // Si no existe el sonido, simplemente no se reproduce (silencioso)
  }

  /**
   * Reproduce música de fondo
   */
  public playMusic(_key?: string): void {
    if (!this.enabled) return;

    if (this.music && !this.music.isPlaying) {
      this.music.play();
    }
  }

  /**
   * Detiene la música de fondo
   */
  public stopMusic(): void {
    if (this.music && this.music.isPlaying) {
      this.music.stop();
    }
  }

  /**
   * Establece el volumen de efectos de sonido
   */
  public setVolume(volume: number): void {
    this.volume = Phaser.Math.Clamp(volume, 0, 1);
    this.sounds.forEach(sound => {
      if ('volume' in sound) {
        (sound as any).volume = this.volume;
      }
    });
  }

  /**
   * Establece el volumen de la música
   */
  public setMusicVolume(volume: number): void {
    this.musicVolume = Phaser.Math.Clamp(volume, 0, 1);
    if (this.music && 'volume' in this.music) {
      (this.music as any).volume = this.musicVolume;
    }
  }

  /**
   * Habilita o deshabilita el audio
   */
  public setEnabled(enabled: boolean): void {
    this.enabled = enabled;
    if (!enabled) {
      this.stopMusic();
    }
  }

  /**
   * Obtiene si el audio está habilitado
   */
  public isEnabled(): boolean {
    return this.enabled;
  }

  /**
   * Reproduce sonido de impacto/daño
   */
  public playHit(): void {
    this.playSound('hit');
  }

  /**
   * Reproduce sonido de power-up recolectado
   */
  public playPowerUp(): void {
    this.playSound('powerup');
  }

  /**
   * Reproduce sonido de victoria
   */
  public playVictory(): void {
    this.playSound('victory');
  }

  /**
   * Reproduce sonido de explosión
   */
  public playExplosion(): void {
    this.playSound('explosion');
  }

  /**
   * Limpia recursos
   */
  public destroy(): void {
    this.stopMusic();
    this.sounds.clear();
  }
}
