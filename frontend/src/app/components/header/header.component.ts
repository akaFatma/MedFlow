import { Component } from '@angular/core'; // Import Component

@Component({
  selector: 'app-header', // Component selector
  standalone: true, // Declare it as standalone// Import FontAwesomeModule for this standalone component
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent {

}
