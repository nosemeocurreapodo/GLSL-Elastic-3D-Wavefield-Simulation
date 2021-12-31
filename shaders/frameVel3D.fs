#version 330 core
layout(location = 0) out vec3 pixel;

in vec2 TexCoords;

uniform sampler3D velxTex;
uniform sampler3D velyTex;
uniform sampler3D velzTex;
uniform sampler3D rhoTex;
uniform sampler3D muTex;
uniform sampler3D lamTex;
uniform sampler2D surfaceTex;

uniform vec3 sourceLoc[40];
uniform vec3 recieverLoc[20];

float atan2(float y, float x)
{
    bool s = (abs(x) > abs(y));
    return mix(3.14/2.0 - atan(x,y), atan(y,x), s);
}

vec3 toCylindrical(vec3 v)
{
  if(length(v) == 0.0)
    return vec3(0.0,0.0,0.0);
	
  float len = length(v);
	
  float z = v.x;
  float rho = sqrt(pow(v.y,2) + pow(v.z,2));
  float theta = atan2(v.z, v.y);
  
  float diffRed = min((2 * 3.14) - abs(theta - 0), abs(theta - 0));
  float diffGreen = min((2 * 3.14) - abs(theta - 3.14*2.0/3.0), abs(theta - 3.14*2.0/3.0));
  float diffBlue = min((2 * 3.14) - abs(theta - 3.14*4.0/3.0), abs(theta - 3.14*4.0/3.0));
  
  float sigma = 3.14*2.0/3.0;
  float red = exp(-pow(diffRed/sigma,2)); //0 pi
  float green = exp(-pow(diffGreen/sigma,2)); // pi/3
  float blue = exp(-pow(diffBlue/sigma,2)); //pi*2/3
  
  //return normalize(vec3(red,green,blue))/2.0;
  
  return 1000000.0*len*normalize(vec3(red,green,blue));
}

vec3 projectToScreen(vec3 v)
{
  //return vec3(v.x, 0.5, v.z);
  //return vec3(v.x, v.y, 0.5);
  return vec3(0.5,v.y, v.z);
}

void main()
{	
    //vec3 TexCoords3D = vec3(TexCoords.x,0.5,1.0-TexCoords.y); //lat-x, depth-y, long-const
	//vec3 TexCoords3D = vec3(TexCoords.y,TexCoords.x,0.5); // lat-y, long-x, depth-const
	vec3 TexCoords3D = vec3(0.5,TexCoords.x,1.0-TexCoords.y);
	
	float rho = (texture(rhoTex, TexCoords3D).x);
	float lam = (texture(lamTex, TexCoords3D).x);
	float mu = (texture(muTex, TexCoords3D).x);
	
	float surface = (texture(surfaceTex, TexCoords3D.xy).x);
	
	vec3 surfaceColor = vec3(0.0,0.0,0.0);
	/*
	if(TexCoords3D.z < surface)
	{
	  float surfaceDamp = 0.5;
	  float d = exp(-pow(surface-TexCoords3D.z,2)/pow(surfaceDamp/depth,2));
	  surfaceColor = vec3(d);
	}
    */
	
	//vec3 mediumColor = vec3(lam*0.00000000001,0.0,0.0);
	//vec3 mediumColor = vec3(mu*0.00000000001,0.0,0.0);
	//vec3 mediumColor = vec3(rho*0.0001,rho*0.0001,rho*0.0001);
	vec3 mediumColor = vec3(rho*0.0001,lam*0.00000000001,mu*0.00000000001);
	//vec3 mediumColor = vec3(0.0,0.0,0.0);
	
	vec3 vel = vec3(texture(velxTex,TexCoords3D).x,texture(velyTex,TexCoords3D).x,texture(velzTex,TexCoords3D).x);
	//vec3 velColor = vec3(0.0,0.0,length(vel)*100000.0);
	//vec3 velColor = vec3(0.0,0.0,abs(vel.z)*100000.0);
	//vec3 velColor = abs(vel)*100000.0;
	vec3 velColor = toCylindrical(vel);
	
	float r = 0.01;
	vec3 sourceColor = vec3(0.0);
	
	for(int i = 0; i < 40; i++)
	{
    vec3 source_pos = projectToScreen(sourceLoc[i]);
	vec3 sourceDiff = TexCoords3D - source_pos;
	float len = length(sourceDiff);
    
	if(len <= r)
	{
	   sourceColor = vec3(1.0,0.0,0.0);
	}
	}
	
    vec3 recieverColor = vec3(0.0);
	for(int i = 0; i < 20; i++)
	{
	  vec3 recieverPos = projectToScreen(recieverLoc[i]);
	  vec3 recieverDiff = TexCoords3D - recieverPos;
	  float len = length(recieverDiff);
    
      if(len <= r)
	  {
	     recieverColor = vec3(0.0,1.0,0.0);
	  }
	}
	
	pixel = velColor + mediumColor + sourceColor + recieverColor + surfaceColor;
}
