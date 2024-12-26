import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BienvenuComponentComponent } from './bienvenu-component.component';

describe('BienvenuComponentComponent', () => {
  let component: BienvenuComponentComponent;
  let fixture: ComponentFixture<BienvenuComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BienvenuComponentComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BienvenuComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
