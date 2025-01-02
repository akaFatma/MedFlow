// import { Component } from '@angular/core';
// import { RouterOutlet } from '@angular/router';
// import { LoginComponent } from './components/auth-card/auth-card.component';

// @Component({
//   selector: 'app-root',
//   imports: [RouterOutlet],
//   templateUrl: './app.component.html',
//   styleUrls: ['./app.component.scss'],
//   template: `<app-login></app-login>`,
//   // template : `<app-add-dpi></app-add-dpi>`,
// })
// export class AppComponent {
//   title = 'gestionDPI';
// }
/* app.component.ts */
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { NgxScannerQrcodeModule, LOAD_WASM } from 'ngx-scanner-qrcode';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  standalone: true,
  imports: [RouterOutlet, CommonModule],
})
export class AppComponent {
  title = 'gestionDPI';
}
