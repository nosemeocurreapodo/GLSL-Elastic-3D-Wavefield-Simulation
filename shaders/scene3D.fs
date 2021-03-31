#version 330 core
layout(location = 0) out vec4 f_color;

in vec3 g_TexCoords;

uniform sampler3D velxTex;
uniform sampler3D velyTex;
uniform sampler3D velzTex;

uniform sampler3D lamTex;

void main()
{
  vec3 vel = vec3(texture(velxTex, g_TexCoords).x, texture(velyTex, g_TexCoords).x, texture(velzTex, g_TexCoords).x);
  vel = vel*1000.0;
  
  float medium = texture(lamTex, g_TexCoords).x;
  float alpha = medium;
  
  
  f_color = vec4(vel+vec3(0.5),0.1);
  //f_color = vec4(medium*0.00000000001, 0.0, 0.0, 1.0);
}
