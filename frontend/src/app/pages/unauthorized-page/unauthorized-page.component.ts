import { Component } from '@angular/core';
import { UnauthorizedComponent } from '../../components/unauthorized/unauthorized.component';

@Component({
  selector: 'app-unauthorized-page',
  imports: [UnauthorizedComponent],
  templateUrl: './unauthorized-page.component.html',
  styleUrl: './unauthorized-page.component.scss'
})
export class UnauthorizedPageComponent {

}
