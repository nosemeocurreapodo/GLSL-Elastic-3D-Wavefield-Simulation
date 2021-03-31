#version 330 core
layout(location = 0) out float upSigmaxx;
layout(location = 1) out float upSigmaxy;
layout(location = 2) out float upSigmaxz;
layout(location = 3) out float upSigmayy;
layout(location = 4) out float upSigmayz;
layout(location = 5) out float upSigmazz;

in vec2 g_TexCoords;
flat in int g_layer;

// texture samplers
uniform sampler3D velxTex;
uniform sampler3D velyTex;
uniform sampler3D velzTex;

uniform sampler3D lamTex;
uniform sampler3D muTex;

uniform float dx;
uniform float dy;
uniform float dz;
uniform float dt;

uniform float ox;
uniform float oy;
uniform float oz;

uniform float surface;

uniform int layer;

void main()
{	
    vec3 Coords3D;
    if(layer < 0)
	  	Coords3D = vec3(gl_FragCoord.xy, g_layer+0.5);
	else
	  	Coords3D = vec3(gl_FragCoord.xy, layer+0.5);
	
	vec3 TexCoords3D = vec3(Coords3D.x*ox, Coords3D.y*oy, Coords3D.z*oz);
	//vec3 TexCoords3D = vec3(g_TexCoords.xy, Coords3D.z/depth);
	
	float c1xy = 9.0/8.0;
    float c2xy = -1.0/24.0;
	
	float c1z = 1.0;
	float c2z = 0.0;
	
	if(TexCoords3D.z > surface + 5*oz || TexCoords3D.z < surface - 5*oz)
	{
		c1z = 9.0/8.0;
		c2z = -1.0/24.0;
	}
	
	//para sigmaxx sigmayy sigmazz
	
    float lam = (texture(lamTex, TexCoords3D).x);
    float mu = (texture(muTex, TexCoords3D).x);	
    float l2m = lam + 2*mu;
	
	float d_velx_dx = c1xy*(texture(velxTex,TexCoords3D+vec3( 0,0,0)).x - texture(velxTex,TexCoords3D+vec3(-ox,0,0)).x);
	d_velx_dx += c2xy*(texture(velxTex,TexCoords3D+vec3( ox,0,0)).x - texture(velxTex,TexCoords3D+vec3(-2*ox,0,0)).x);
	d_velx_dx /= dx;
	
	float d_vely_dy = c1xy*(texture(velyTex,TexCoords3D+vec3(0, 0,0)).x - texture(velyTex,TexCoords3D+vec3(0,-oy,0)).x);
	d_vely_dy += c2xy*(texture(velyTex,TexCoords3D+vec3(0, oy,0)).x - texture(velyTex,TexCoords3D+vec3(0,-2*oy,0)).x);
	d_vely_dy /= dy;
	
	float d_velz_dz = c1z*(texture(velzTex,TexCoords3D+vec3(0,0,0)).x - texture(velzTex,TexCoords3D+vec3(0,0,-oz)).x);
	d_velz_dz += c2z*(texture(velzTex,TexCoords3D+vec3(0,0, oz)).x - texture(velzTex,TexCoords3D+vec3(0,0,-2*oz)).x);
	d_velz_dz /= dz;
		
	upSigmaxx = (l2m*d_velx_dx+lam*(d_velz_dz+d_vely_dy))*dt;
	upSigmayy = (l2m*d_vely_dy+lam*(d_velz_dz+d_velx_dx))*dt;
	upSigmazz = (l2m*d_velz_dz+lam*(d_vely_dy+d_velx_dx))*dt;

	//para sigmaxy
	  
	float muxy = (texture(muTex, TexCoords3D + vec3(0.5*ox,0.5*oy,0.0)).x);
	
	float d_vely_dx = c1xy*(texture(velyTex,TexCoords3D+vec3( ox,0,0)).x - texture(velyTex,TexCoords3D+vec3( 0,0,0)).x);
	d_vely_dx += c2xy*(texture(velyTex,TexCoords3D+vec3( 2*ox,0,0)).x - texture(velyTex,TexCoords3D+vec3(-ox,0,0)).x);
	d_vely_dx /= dx;
	
	float d_velx_dy = c1xy*(texture(velxTex,TexCoords3D+vec3(0, oy,0)).x - texture(velxTex,TexCoords3D+vec3(0, 0,0)).x);
	d_velx_dy += c2xy*(texture(velxTex,TexCoords3D+vec3(0, 2*oy,0)).x - texture(velxTex,TexCoords3D+vec3(0,-oy,0)).x);
	d_velx_dy /= dy;
	  	
	upSigmaxy = (muxy*(d_velx_dy+d_vely_dx))*dt;

	//para sigmaxz
	  
	float muxz = (texture(muTex, TexCoords3D + vec3(0.5*ox,0.0,0.5*oz)).x);
    
	float d_velx_dz = c1z*(texture(velxTex,TexCoords3D+vec3(0,0, oz)).x - texture(velxTex,TexCoords3D+vec3(0,0, 0)).x);
	d_velx_dz += c2z*(texture(velxTex,TexCoords3D+vec3(0,0, 2*oz)).x - texture(velxTex,TexCoords3D+vec3(0,0,-oz)).x);
	d_velx_dz /= dz;
	
	float d_velz_dx = c1xy*(texture(velzTex,TexCoords3D+vec3( ox,0,0)).x - texture(velzTex,TexCoords3D+vec3( 0,0,0)).x);
	d_velz_dx += c2xy*(texture(velzTex,TexCoords3D+vec3( 2*ox,0,0)).x - texture(velzTex,TexCoords3D+vec3(-ox,0,0)).x);
	d_velz_dx /= dx;
	  
	upSigmaxz = (muxz*(d_velx_dz+d_velz_dx))*dt;


	//para sigmayz
	  
	float muyz = (texture(muTex, TexCoords3D + vec3(0.0,0.5*oy,0.5*oz)).x);
		
	float d_vely_dz = c1z*(texture(velyTex,TexCoords3D+vec3(0,0, oz)).x - texture(velyTex,TexCoords3D+vec3(0,0, 0)).x);
	d_vely_dz += c2z*(texture(velyTex,TexCoords3D+vec3(0,0, 2*oz)).x - texture(velyTex,TexCoords3D+vec3(0,0,-oz)).x);
	d_vely_dz /= dz;
	
	float d_velz_dy = c1xy*(texture(velzTex,TexCoords3D+vec3(0, oy, 0)).x - texture(velzTex,TexCoords3D+vec3(0, 0, 0)).x);
	d_velz_dy += c2xy*(texture(velzTex,TexCoords3D+vec3(0, 2*oy, 0)).x - texture(velzTex,TexCoords3D+vec3(0,-oy, 0)).x);
	d_velz_dy /= dy;
	   
	upSigmayz = (muyz*(d_vely_dz+d_velz_dy))*dt;
}
