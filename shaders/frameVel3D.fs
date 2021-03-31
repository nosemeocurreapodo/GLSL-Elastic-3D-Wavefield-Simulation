#version 330 core
layout(location = 0) out vec3 pixel;

in vec2 TexCoords;

uniform sampler3D velxTex;
uniform sampler3D velyTex;
uniform sampler3D velzTex;
uniform sampler3D invRhoTex;
uniform sampler3D muTex;
uniform sampler3D lamTex;

uniform float width;
uniform float height;
uniform float depth;

uniform vec3 sourceLoc;
uniform vec3 recieverLoc[20];

vec3 projectToScreen(vec3 v)
{
  //return vec3(v.x, 0.5, v.z);
  //return vec3(v.x, v.y, 0.5);
  return vec3(0.5,v.y, v.z);
}

void main()
{	
    //vec3 TexCoords3D = vec3(TexCoords.x,0.5,1.0-TexCoords.y); //lat-x, depth-y, long-const
	vec3 TexCoords3D = vec3(0.5,TexCoords.x,1.0-TexCoords.y);
	//vec3 TexCoords3D = vec3(TexCoords.y,TexCoords.x,0.5); // lat-y, long-x, depth-const

	float invRho = (texture(invRhoTex, TexCoords3D).x);
	float lam = (texture(lamTex, TexCoords3D).x);
	float mu = (texture(muTex, TexCoords3D).x);
	
	vec3 mediumColor = vec3(lam*0.00000000001,0.0,0.0);
	//vec3 mediumColor = vec3(mu*0.0000000001,0.0,0.0);
	
	vec3 vel = vec3(texture(velxTex,TexCoords3D-vec3(0.5/width,0.0,0.0)).x,texture(velyTex,TexCoords3D-vec3(0.0,0.5/height,0.0)).x,texture(velzTex,TexCoords3D-vec3(0.0,0.0,0.5/depth)).x);
	vec3 velColor = vec3(0.0,0.0,length(vel)*10000.0);
	
	float r = 1.0;
	vec3 sourceColor = vec3(0.0);
	
    vec3 source_pos = projectToScreen(sourceLoc);
	vec3 sourceDiff = TexCoords3D - source_pos;
	sourceDiff.x *= width;
	sourceDiff.y *= height;
	sourceDiff.z *= depth;
	float len = length(sourceDiff);
    
	if(len <= r)
	{
	   sourceColor = vec3(0.0,1.0,0.0);
	}
	
    vec3 recieverColor = vec3(0.0);
	for(int i = 0; i < 20; i++)
	{
	  vec3 recieverPos = projectToScreen(recieverLoc[i]);
	  vec3 recieverDiff = TexCoords3D - recieverPos;
	  recieverDiff.x *= width;
	  recieverDiff.y *= height;
	  recieverDiff.z *= depth;
	  float len = length(recieverDiff);
    
      if(len <= r)
	  {
	     recieverColor = vec3(0.0,1.0,0.0);
	  }
	}
	
	pixel = velColor + mediumColor + sourceColor + recieverColor;
}
