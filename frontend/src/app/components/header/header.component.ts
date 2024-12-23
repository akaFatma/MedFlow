import { Component } from '@angular/core'; // Import Component
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'; // Import FontAwesomeModule
import { faUser, faBell } from '@fortawesome/free-solid-svg-icons'; // Import the icons

@Component({
  selector: 'app-header', // Component selector
  standalone: true, // Declare it as standalone
  imports: [FontAwesomeModule], // Import FontAwesomeModule for this standalone component
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {
  faUser = faUser;
  faBell = faBell;
  
}
