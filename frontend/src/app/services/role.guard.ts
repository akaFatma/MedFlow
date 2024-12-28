import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
  })
  export class RoleGuard implements CanActivate {
  
    constructor(private authService: AuthService, private router: Router) {}
  
    canActivate(
      route: ActivatedRouteSnapshot,
      state: RouterStateSnapshot
      
    ): Observable<boolean> | Promise<boolean> | boolean {
      if (!this.authService.isAuthentificated()) {
        this.router.navigate(['/login']);
        return false;
      }
      
      const userRole = this.authService.getUserRole();
      const expectedRoles = route.data['roles'] || [route.data['role']];
  

      if (expectedRoles.includes(userRole)) {
        return true;
      } else {
        this.router.navigate(['/unauthorized']);
        return false;
      }

    }
  }