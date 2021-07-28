# Compilación de Assets

## Preparación

La compilación de assets requiere [node][node-dowload].

```bash
# Ir al directorio de assets
cd front/assets/

# Si está instalado nvm - https://github.com/nvm-sh/nvm
nvm use

# Instalar dependencias
npm install
```

## Compilación de assets

```bash
# Ir al directorio de assets
cd front/assets/

# Correr webpack
npm run build
# o también, correr webpack en watch-mode
# OJO que no se recarga el navegador en cada cambio!
npm run dev
```

## Integración con Django

Para utilizar los assets generados se utiliza
la librería de python [django-manifest-loader][djm]
y el plugin de webpack [webpack-manifest-plugin][wmp].

Para utilizar un asset en un template, se utiliza

```django
{% load manifest %}
<link rel="stylesheet" href="{% manifest 'style_file.css' %}">
<script type="text/javascript" src="{% manifest 'script_file.js' %}"></script>
```

donde `script_file` y `style_file` son nombres de entradas
especificadas en [`webpack.config.js`](./webpack.config.js).


[node-dowload]: https://nodejs.org/es/download/current/
[webpack]: (https://webpack.js.org/)
[djm]: https://github.com/shonin/django-manifest-loader
[wmp]: https://github.com/shellscape/webpack-manifest-plugin
