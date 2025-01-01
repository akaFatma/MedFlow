import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideRouter } from '@angular/router';
import { provideHttpClient, HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { routes } from './app/app.routes';
import { AuthInterceptor } from './app/services/auth.interceptor';
import { importProvidersFrom } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'; // Import FontAwesomeModule

// Bootstrapping the application
bootstrapApplication(AppComponent, {
  providers: [
    // Import HttpClientModule correctly using importProvidersFrom
    importProvidersFrom(HttpClientModule),

    // Provide FontAwesomeModule if you need it globally
    importProvidersFrom(FontAwesomeModule),

    // Provide the HttpClient and set up the interceptor
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },

    // Provide router configuration
    provideRouter(routes),
  ],
}).catch((err) => console.error(err));
