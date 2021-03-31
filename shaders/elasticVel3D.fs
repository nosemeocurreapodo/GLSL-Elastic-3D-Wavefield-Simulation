#version 330 core
layout(location = 0) out float upVelx;
layout(location = 1) out float upVely;
layout(location = 2) out float upVelz;

in vec2 g_TexCoords;
flat in int g_layer;

// texture samplers
uniform sampler3D sigmaxxTex;
uniform sampler3D sigmaxyTex;
uniform sampler3D sigmaxzTex;
uniform sampler3D sigmayyTex;
uniform sampler3D sigmayzTex;
uniform sampler3D sigmazzTex;

uniform sampler3D invRhoTex;

uniform sampler3D fxTex;
uniform sampler3D fyTex;
uniform sampler3D fzTex;

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
	//vec3 TexCoords3D = vec3(g_TexCoords.xy, Coords3D.z*oz);
	
	float c1xy = 9.0/8.0;
    float c2xy = -1.0/24.0;
	
	float c1z = 1.0;
	float c2z = 0.0;
	
	if(TexCoords3D.z > surface + 5*oz || TexCoords3D.z < surface - 5*oz)
	{
		c1z = 9.0/8.0;
		c2z = -1.0/24.0;
	}
	
	//para vx 

	float invRhox = (texture(invRhoTex, TexCoords3D + vec3(0.5*ox,0.0,0.0)).x);
	
	float d_sigmaxx_dx = c1xy*(texture(sigmaxxTex,TexCoords3D+vec3( ox,0,0)).x - texture(sigmaxxTex,TexCoords3D+vec3( 0,0,0)).x);
	d_sigmaxx_dx +=  c2xy*(texture(sigmaxxTex,TexCoords3D+vec3( 2*ox,0,0)).x - texture(sigmaxxTex,TexCoords3D+vec3(-ox,0,0)).x);
	d_sigmaxx_dx /= dx;
	
	float d_sigmaxy_dy = c1xy*(texture(sigmaxyTex,TexCoords3D+vec3(0, 0,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(0,-oy,0)).x);
	d_sigmaxy_dy +=  c2xy*(texture(sigmaxyTex,TexCoords3D+vec3(0, oy,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(0,-2*oy,0)).x);
	d_sigmaxy_dy /= dy;
	
	float d_sigmaxz_dz = c1z*(texture(sigmaxzTex,TexCoords3D+vec3(0,0, 0)).x - texture(sigmaxzTex,TexCoords3D+vec3(0,0,-oz)).x);
	d_sigmaxz_dz +=  c2z*(texture(sigmaxzTex,TexCoords3D+vec3(0,0, oz)).x - texture(sigmaxzTex,TexCoords3D+vec3(0,0,-2*oz)).x);
	d_sigmaxz_dz /= dz;
	 	
	upVelx = (d_sigmaxx_dx+d_sigmaxy_dy+d_sigmaxz_dz + texelFetch(fxTex,ivec3(Coords3D),0).x)*dt*invRhox;

	//para vy

	float invRhoy = (texture(invRhoTex, TexCoords3D + vec3(0.0,0.5*oy,0.0)).x);
	  
	float d_sigmaxy_dx = c1xy*(texture(sigmaxyTex,TexCoords3D+vec3( 0,0,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(-ox,0,0)).x);
	d_sigmaxy_dx +=  c2xy*(texture(sigmaxyTex,TexCoords3D+vec3( ox,0,0)).x - texture(sigmaxyTex,TexCoords3D+vec3(-2*ox,0,0)).x);
	d_sigmaxy_dx /= dx;
	
	float d_sigmayy_dy = c1xy*(texture(sigmayyTex,TexCoords3D+vec3(0, oy,0)).x - texture(sigmayyTex,TexCoords3D+vec3(0, 0,0)).x);
	d_sigmayy_dy +=  c2xy*(texture(sigmayyTex,TexCoords3D+vec3(0, 2*oy,0)).x - texture(sigmayyTex,TexCoords3D+vec3(0,-oy,0)).x);
	d_sigmayy_dy /= dy;
	
	float d_sigmayz_dz = c1z*(texture(sigmayzTex,TexCoords3D+vec3(0,0, 0)).x - texture(sigmayzTex,TexCoords3D+vec3(0,0,-oz)).x);
	d_sigmayz_dz +=  c2z*(texture(sigmayzTex,TexCoords3D+vec3(0,0, oz)).x - texture(sigmayzTex,TexCoords3D+vec3(0,0,-2*oz)).x);
	d_sigmayz_dz /= dz;
	
	upVely = (d_sigmaxy_dx+d_sigmayy_dy+d_sigmayz_dz + texelFetch(fyTex,ivec3(Coords3D),0).x)*dt*invRhoy;

	//para vz
	
	float invRhoz = (texture(invRhoTex, TexCoords3D + vec3(0.0,0.0,0.5*oz)).x);
	
	float d_sigmaxz_dx = c1xy*(texture(sigmaxzTex,TexCoords3D+vec3( 0,0,0)).x - texture(sigmaxzTex,TexCoords3D+vec3(-ox,0,0)).x);
	d_sigmaxz_dx +=  c2xy*(texture(sigmaxzTex,TexCoords3D+vec3( ox,0,0)).x - texture(sigmaxzTex,TexCoords3D+vec3(-2*ox,0,0)).x);
	d_sigmaxz_dx /= dx;
	
	float d_sigmayz_dy = c1xy*(texture(sigmayzTex,TexCoords3D+vec3(0, 0,0)).x - texture(sigmayzTex,TexCoords3D+vec3(0,-oy,0)).x);
	d_sigmayz_dy +=  c2xy*(texture(sigmayzTex,TexCoords3D+vec3(0, oy,0)).x - texture(sigmayzTex,TexCoords3D+vec3(0,-2*oy,0)).x);
	d_sigmayz_dy /= dy;
	
	float d_sigmazz_dz = c1z*(texture(sigmazzTex,TexCoords3D+vec3(0,0, oz)).x - texture(sigmazzTex,TexCoords3D+vec3(0,0, 0)).x);
	d_sigmazz_dz +=  c2z*(texture(sigmazzTex,TexCoords3D+vec3(0,0, 2*oz)).x - texture(sigmazzTex,TexCoords3D+vec3(0,0,-oz)).x);
	d_sigmazz_dz /= dz;
	
	upVelz = (d_sigmaxz_dx+d_sigmayz_dy+d_sigmazz_dz + texelFetch(fzTex,ivec3(Coords3D),0).x)*dt*invRhoz;

}
