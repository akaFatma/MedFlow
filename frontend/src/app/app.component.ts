import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';  // Import RouterOutlet

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],  // Import RouterOutlet
  templateUrl: './app.component.html', // Use external template file
  styleUrls: ['./app.component.scss'],  // Correct typo in styleUrls
})
export class AppComponent {
  title = 'gestionDPI';
}
