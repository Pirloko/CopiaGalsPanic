# 🚀 Guía de Despliegue en Netlify

Esta guía te ayudará a desplegar el proyecto Gals Panic Phaser 3 en Netlify.

## 📋 Requisitos Previos

- Cuenta en [Netlify](https://www.netlify.com/)
- Proyecto subido a GitHub (ya completado ✅)

## 🎯 Opción 1: Despliegue desde GitHub (Recomendado)

### Pasos:

1. **Inicia sesión en Netlify**
   - Ve a [app.netlify.com](https://app.netlify.com/)
   - Inicia sesión con tu cuenta de GitHub

2. **Nuevo sitio desde Git**
   - Haz clic en "Add new site" → "Import an existing project"
   - Selecciona "GitHub" y autoriza Netlify
   - Busca y selecciona el repositorio: `Pirloko/CopiaGalsPanic`

3. **Configuración del Build**
   - Netlify detectará automáticamente la configuración desde `netlify.toml`
   - **Build command**: `npm run build` (ya configurado)
   - **Publish directory**: `dist` (ya configurado)
   - Haz clic en "Deploy site"

4. **Espera el despliegue**
   - Netlify instalará dependencias y construirá el proyecto
   - El proceso tomará 1-2 minutos
   - Verás el progreso en tiempo real

5. **¡Listo!**
   - Tu juego estará disponible en una URL como: `https://random-name-123.netlify.app`
   - Puedes personalizar el nombre en: Site settings → Change site name

## 🎯 Opción 2: Despliegue Manual (Arrastrar y Soltar)

Si prefieres desplegar manualmente:

1. **Construye el proyecto localmente**:
   ```bash
   npm run build
   ```

2. **Ve a Netlify**
   - Inicia sesión en [app.netlify.com](https://app.netlify.com/)
   - Arrastra la carpeta `dist` a la zona de "Deploy"

3. **¡Listo!**
   - Tu sitio estará disponible inmediatamente

## ⚙️ Configuración Personalizada

### Cambiar el nombre del sitio

1. Ve a **Site settings** → **Change site name**
2. Elige un nombre único (ej: `gals-panic-game`)
3. Tu URL será: `https://gals-panic-game.netlify.app`

### Configurar dominio personalizado

1. Ve a **Site settings** → **Domain management**
2. Haz clic en **Add custom domain**
3. Sigue las instrucciones para configurar tu dominio

### Variables de entorno (si las necesitas)

1. Ve a **Site settings** → **Environment variables**
2. Añade variables si tu proyecto las requiere

## 📝 Archivos de Configuración

El proyecto incluye `netlify.toml` con:
- ✅ Configuración de build automática
- ✅ Redirecciones para SPA
- ✅ Headers de seguridad
- ✅ Optimización de caché

## 🔄 Actualizaciones Automáticas

Con la **Opción 1** (GitHub), cada vez que hagas `git push`:
- Netlify detectará los cambios automáticamente
- Reconstruirá y redesplegará el sitio
- Tus cambios estarán en vivo en minutos

## 🐛 Solución de Problemas

### El build falla
- Verifica que `npm run build` funciona localmente
- Revisa los logs de build en Netlify
- Asegúrate de que todas las dependencias están en `package.json`

### El juego no carga
- Verifica que el directorio `dist` contiene `index.html`
- Revisa la consola del navegador para errores
- Asegúrate de que los assets están en la ruta correcta

### Problemas con rutas
- El archivo `netlify.toml` ya incluye redirecciones para SPA
- Si persisten problemas, verifica la configuración de `[[redirects]]`

## 📊 Monitoreo

Netlify proporciona:
- **Analytics**: Estadísticas de visitas
- **Forms**: Si necesitas formularios
- **Functions**: Para backend serverless (opcional)

## 🎉 ¡Listo para Jugar!

Una vez desplegado, tu juego estará disponible para todo el mundo en:
`https://tu-sitio.netlify.app`

---

**Nota**: El primer despliegue puede tardar 2-3 minutos. Los siguientes serán más rápidos gracias al caché de Netlify.

