import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RedigerSoinsComponent } from './rediger-soins.component';

describe('RedigerSoinsComponent', () => {
  let component: RedigerSoinsComponent;
  let fixture: ComponentFixture<RedigerSoinsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RedigerSoinsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RedigerSoinsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
