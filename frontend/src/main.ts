// import { bootstrapApplication } from '@angular/platform-browser';
// import { AppComponent } from './app/app.component';
// import { provideRouter } from '@angular/router';
// import { provideHttpClient, HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
// import { routes } from './app/app.routes';
// import { AuthInterceptor } from './app/services/auth.interceptor';
// import { importProvidersFrom } from '@angular/core';

// bootstrapApplication(AppComponent, {
//   providers: [
//     importProvidersFrom(HttpClientModule),

//     { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },

//     provideRouter(routes),
//   ],
// }).catch((err) => console.error(err));

import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig).catch((err) =>
  console.error(err)
);
