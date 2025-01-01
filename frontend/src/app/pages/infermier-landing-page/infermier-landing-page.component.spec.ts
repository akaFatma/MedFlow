import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfermierLandingPageComponent } from './infermier-landing-page.component';

describe('InfermierLandingPageComponent', () => {
  let component: InfermierLandingPageComponent;
  let fixture: ComponentFixture<InfermierLandingPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfermierLandingPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InfermierLandingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
