# Užduotys

### 1
sukurkite flask registracijos puslapį, kuriame būtų panaudotas Bootstrap, veikianti žemiau nurodyta forma su csrf apsauga, ir sėkmės puslapis, kuriame bus išgaudytos visos laukų reikšmės. Apdėliokite formą validacijos filtrais, ir padarykite taip, kad nesėkmės atveju vartotojas matytų klaidas. Kadangi šablonai bus 2 (forma ir success puslapis), sukurkite base.httml, iš kurios jie paveldėtų titulinę dalį ir JS nuorodas.


```html
<form>
  <div class="form-row">
    <div class="form-group col-md-6">
      <label for="inputEmail4">Email</label>
      <input type="email" class="form-control" id="inputEmail4">
    </div>
    <div class="form-group col-md-6">
      <label for="inputPassword4">Password</label>
      <input type="password" class="form-control" id="inputPassword4">
    </div>
  </div>
  <div class="form-group">
    <label for="inputAddress">Address</label>
    <input type="text" class="form-control" id="inputAddress" placeholder="1234 Main St">
  </div>
  <div class="form-group">
    <label for="inputAddress2">Address 2</label>
    <input type="text" class="form-control" id="inputAddress2" placeholder="Apartment, studio, or floor">
  </div>
  <div class="form-row">
    <div class="form-group col-md-6">
      <label for="inputCity">City</label>
      <input type="text" class="form-control" id="inputCity">
    </div>
    <div class="form-group col-md-4">
      <label for="inputState">State</label>
      <select id="inputState" class="form-control">
        <option selected>Choose...</option>
        <option>...</option>
      </select>
    </div>
    <div class="form-group col-md-2">
      <label for="inputZip">Zip</label>
      <input type="text" class="form-control" id="inputZip">
    </div>
  </div>
  <div class="form-group">
    <div class="form-check">
      <input class="form-check-input" type="checkbox" id="gridCheck">
      <label class="form-check-label" for="gridCheck">
        Check me out
      </label>
    </div>
  </div>
  <button type="submit" class="btn btn-primary">Sign in</button>
</form>

```

### 2

* sugalvokite būdą, kaip išsaugoti duomenis į json failą, kurį galima naudoti kaip duomenų bazę. 
* sukurkite šabloną adresatai, kuriame bus email reikšmių sąrašas
* paspaudus ant email adreso turėsime pakliųti į dinaminę nuorodą, kurioje matysis visi likusieji anketos duomenys. 

