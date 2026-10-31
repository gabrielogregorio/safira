import { aimAxis, buildGemMesh, easeAxis, RESTING_AXIS, rotationMatrix } from './gemMath';

interface GemOptions {
  size: number;
  animate: boolean;
  onLost: () => void;
}

const MAXIMUM_PIXEL_RATIO = 2;
const SPIN_PER_SECOND = 0.9;
const MILLISECONDS_PER_SECOND = 1000;

const VERTEX_SHADER = `#version 300 es
in vec3 position;
in vec3 normal;
uniform mat3 rotation;
out vec3 worldPosition;
out vec3 worldNormal;

void main() {
  worldPosition = rotation * position;
  worldNormal = rotation * normal;
  float perspective = (4.0 - worldPosition.z) / 4.0;
  gl_Position = vec4(worldPosition.xy * 0.8, 0.0, perspective);
}`;

const FRAGMENT_SHADER = `#version 300 es
precision highp float;
in vec3 worldPosition;
in vec3 worldNormal;
uniform float frontPass;
out vec4 color;

vec3 sky(vec3 direction) {
  float height = smoothstep(-0.9, 0.8, direction.y);
  vec3 base = mix(vec3(0.02, 0.1, 0.45), vec3(0.85, 0.95, 1.0), height);
  float bands = pow(max(sin(direction.x * 11.0 + direction.y * 7.0 + direction.z * 5.0), 0.0), 5.0);

  return base + bands * vec3(0.6, 0.85, 1.0) * 0.9;
}

float flash(vec3 reflected, vec3 light, float sharpness) {
  return pow(max(dot(reflected, normalize(light)), 0.0), sharpness);
}

void main() {
  vec3 facing = normalize(worldNormal) * (gl_FrontFacing ? 1.0 : -1.0);
  vec3 view = normalize(vec3(0.0, 0.0, 4.0) - worldPosition);
  vec3 reflected = reflect(-view, facing);
  vec3 refracted = refract(-view, facing, 1.0 / 1.77);
  float glow = dot(sky(refracted), vec3(0.3, 0.5, 0.2));
  vec3 body = mix(vec3(0.0, 0.015, 0.2), vec3(0.08, 0.34, 1.0), smoothstep(0.22, 0.62, glow));
  float fresnel = pow(1.0 - max(dot(facing, view), 0.0), 2.5);

  // The far side shows through the near side, as light bouncing inside the stone.
  if (frontPass < 0.5) {
    vec3 inner = body + sky(reflected) * vec3(0.05, 0.14, 0.6) * 0.55;
    color = vec4(inner + vec3(0.1, 0.35, 1.0) * flash(reflected, vec3(0.1, 0.6, -0.8), 16.0), 1.0);

    return;
  }

  vec3 surface = body * 0.75 + sky(reflected) * vec3(0.35, 0.5, 0.95) * (0.07 + 0.6 * fresnel);
  surface += vec3(1.0) * flash(reflected, vec3(0.5, 0.8, 0.6), 40.0) * 1.6;
  surface += vec3(0.8, 0.92, 1.0) * flash(reflected, vec3(-0.7, 0.3, 0.65), 60.0) * 1.3;
  surface += vec3(0.7, 0.85, 1.0) * flash(reflected, vec3(0.1, -0.5, 0.85), 80.0);
  float alpha = 0.58 + 0.4 * max(fresnel, min(dot(surface, vec3(0.33)) - 0.9, 1.0));
  color = vec4(surface * alpha, alpha);
}`;

const compile = (gl: WebGL2RenderingContext, kind: number, source: string): WebGLShader | null => {
  const shader = gl.createShader(kind);

  if (shader === null) {
    return null;
  }

  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  return gl.getShaderParameter(shader, gl.COMPILE_STATUS) === true ? shader : null;
};

const linkProgram = (gl: WebGL2RenderingContext): WebGLProgram | null => {
  const vertex = compile(gl, gl.VERTEX_SHADER, VERTEX_SHADER);
  const fragment = compile(gl, gl.FRAGMENT_SHADER, FRAGMENT_SHADER);
  const program = gl.createProgram();

  if (vertex === null || fragment === null) {
    return null;
  }

  gl.attachShader(program, vertex);
  gl.attachShader(program, fragment);
  gl.linkProgram(program);

  return gl.getProgramParameter(program, gl.LINK_STATUS) === true ? program : null;
};

const bindAttribute = (gl: WebGL2RenderingContext, program: WebGLProgram, name: string, data: Float32Array): void => {
  const location = gl.getAttribLocation(program, name);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW);
  gl.enableVertexAttribArray(location);
  gl.vertexAttribPointer(location, 3, gl.FLOAT, false, 0, 0);
};

// Returns null when the browser has no WebGL 2, so that the caller can show the flat logo.
export const startGem = (canvas: HTMLCanvasElement, { size, animate, onLost }: GemOptions): (() => void) | null => {
  const gl = canvas.getContext('webgl2', { alpha: true, antialias: true, premultipliedAlpha: true });

  if (gl === null) {
    return null;
  }

  const program = linkProgram(gl);

  if (program === null) {
    return null;
  }

  const pixels = Math.round(size * Math.min(window.devicePixelRatio, MAXIMUM_PIXEL_RATIO));
  canvas.width = pixels;
  canvas.height = pixels;

  const mesh = buildGemMesh();
  const vertexCount = mesh.positions.length / 3;
  const rotationUniform = gl.getUniformLocation(program, 'rotation');
  const frontPassUniform = gl.getUniformLocation(program, 'frontPass');
  let axis = RESTING_AXIS;
  let target = RESTING_AXIS;
  let spin = 0;
  let previousTime = performance.now();
  let frame = 0;

  gl.useProgram(program);
  bindAttribute(gl, program, 'position', mesh.positions);
  bindAttribute(gl, program, 'normal', mesh.normals);
  gl.viewport(0, 0, pixels, pixels);
  gl.clearColor(0, 0, 0, 0);
  gl.enable(gl.CULL_FACE);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

  // The gem is convex: drawing the far side and then the near side needs no depth buffer.
  const draw = (): void => {
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniformMatrix3fv(rotationUniform, false, rotationMatrix(axis, spin));
    gl.cullFace(gl.FRONT);
    gl.uniform1f(frontPassUniform, 0);
    gl.drawArrays(gl.TRIANGLES, 0, vertexCount);
    gl.cullFace(gl.BACK);
    gl.uniform1f(frontPassUniform, 1);
    gl.drawArrays(gl.TRIANGLES, 0, vertexCount);
  };

  const advance = (now: number): void => {
    const seconds = (now - previousTime) / MILLISECONDS_PER_SECOND;
    previousTime = now;
    axis = easeAxis(axis, target, seconds);
    spin += seconds * SPIN_PER_SECOND;
    draw();
    frame = requestAnimationFrame(advance);
  };

  const followPointer = (event: PointerEvent): void => {
    const box = canvas.getBoundingClientRect();
    target = aimAxis(event.clientX - box.left - box.width / 2, event.clientY - box.top - box.height / 2);
  };

  const handleLost = (): void => {
    cancelAnimationFrame(frame);
    onLost();
  };

  canvas.addEventListener('webglcontextlost', handleLost);

  if (animate) {
    window.addEventListener('pointermove', followPointer, { passive: true });
    frame = requestAnimationFrame(advance);
  } else {
    draw();
  }

  return () => {
    cancelAnimationFrame(frame);
    window.removeEventListener('pointermove', followPointer);
    canvas.removeEventListener('webglcontextlost', handleLost);
  };
};
