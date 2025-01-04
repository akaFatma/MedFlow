import { ApplicationConfig } from '@angular/core';
import { provideHttpClient, withInterceptorsFromDi } from '@angular/common/http';  // Utilisez provideHttpClient
import { provideServerRendering } from '@angular/platform-server';
import { provideServerRoutesConfig } from '@angular/ssr';
import { appConfig } from './app.config';
import { serverRoutes } from './app.routes.server';

const serverConfig: ApplicationConfig = {
  providers: [
    provideServerRendering(),
    provideServerRoutesConfig(serverRoutes),
    provideHttpClient(withInterceptorsFromDi()),  // Remplacez HttpClientModule par provideHttpClient
  ],
};

export const config = { ...appConfig, ...serverConfig };
