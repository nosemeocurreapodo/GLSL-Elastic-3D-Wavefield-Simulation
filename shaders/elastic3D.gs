#version 330 core
layout (triangles) in;
layout (triangle_strip, max_vertices = 3) out;

in vec2 v_TexCoords[];
flat in int v_layer[];
out vec2 g_TexCoords;
flat out int g_layer;

void main()
{

  for(int i = 0; i < 3; i++)
  {
    gl_Layer = v_layer[i];
    g_layer = v_layer[i];

    gl_Position = gl_in[i].gl_Position;
    g_TexCoords = v_TexCoords[i];
    EmitVertex();
  }

  EndPrimitive();
}

