import { bootstrapApplication } from '@angular/platform-browser';
import { AppComponent } from './app/app.component';
import { provideRouter } from '@angular/router';
import { provideHttpClient, HTTP_INTERCEPTORS } from '@angular/common/http';
import { routes } from './app/app.routes';
import { AuthInterceptor } from './app/services/auth.interceptor';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'; // Import FontAwesomeModule

bootstrapApplication(AppComponent, {
  providers: [
    provideHttpClient(),
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    provideRouter(routes),
    FontAwesomeModule,  // Ensure FontAwesomeModule is here if you need it globally
  ],
}).catch((err) => console.error(err));
