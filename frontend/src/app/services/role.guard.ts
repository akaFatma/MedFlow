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
      const expectedRole = route.data['role'];
      const userRole = this.authService.getUserRole();
  
      if (userRole === expectedRole) {
        return true;
      } else {
        this.router.navigate(['/unauthorized']);
        return false;
      }
    }
  }