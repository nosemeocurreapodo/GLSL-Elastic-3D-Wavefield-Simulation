#version 330 core
layout (triangles) in;
//layout (line_strip, max_vertices = 2) out;
layout (triangle_strip, max_vertices = 3) out;

in vec3 v_TexCoords[];
out vec3 g_TexCoords;

void main()
{

  g_TexCoords = v_TexCoords[0];
  gl_Position = gl_in[0].gl_Position;
  EmitVertex();
  
  g_TexCoords = v_TexCoords[1];
  gl_Position = gl_in[1].gl_Position;
  EmitVertex();
  
  g_TexCoords = v_TexCoords[2];
  gl_Position = gl_in[2].gl_Position;
  EmitVertex();
  
  EndPrimitive();

  

  
  
  /*
  float alpha = 1.0;	
  vec3 TexCoords3D = vec3(0.0);
  vec3 vel = vec3(0.0);
  
  TexCoords3D = v_TexCoords[2];
  vel = vec3(texture(velxTex, TexCoords3D).x, texture(velyTex, TexCoords3D).x, texture(velzTex, TexCoords3D).x);
  gl_Position = gl_in[2].gl_Position;
  EmitVertex();
  
  TexCoords3D = v_TexCoords[1];
  vel = vec3(texture(velxTex, TexCoords3D).x, texture(velyTex, TexCoords3D).x, texture(velzTex, TexCoords3D).x);
  gl_Position = gl_in[1].gl_Position;
  EmitVertex();
  
  EndPrimitive();
  
  TexCoords3D = v_TexCoords[0];
  vel = vec3(texture(velxTex, TexCoords3D).x, texture(velyTex, TexCoords3D).x, texture(velzTex, TexCoords3D).x);
  gl_Position = gl_in[0].gl_Position;
  EmitVertex();
  
  TexCoords3D = v_TexCoords[2];
  vel = vec3(texture(velxTex, TexCoords3D).x, texture(velyTex, TexCoords3D).x, texture(velzTex, TexCoords3D).x);
  gl_Position = gl_in[2].gl_Position;
  EmitVertex();
  
  EndPrimitive();  
  */
  
}

