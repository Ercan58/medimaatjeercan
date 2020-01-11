using System;
using testApiMac.Model;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Collections;

namespace testApiMac.Controllers
{
    [Route("api/[Controller]")]
    [ApiController]
    public class PersonsController : ControllerBase
    {
        private readonly ercansjoeppiedb _Context;

        public PersonsController(ercansjoeppiedb context) {
            _Context = context;

        }

        //GET API PERSONS
        [HttpGet]
        public ActionResult<IEnumerable<Persons>> GetPersons(string naam)
        {
            

            if (naam == null)
            {
                return _Context.Persons;
            }
            var persons = _Context.Persons.FirstOrDefault(ba=>ba.Naam == naam);
            var enumerable = new[] { persons };
            return enumerable;

        }

        [HttpGet("{id}")]
        public ActionResult<Persons> GetPerson(int id) {
            var persons = _Context.Persons.Find(id);
            if (persons == null)
            {
                return NotFound();
            }

            return persons;
        }






        [HttpPost]
        public ActionResult<Persons> PostPersons(Persons person)
        {
            _Context.Persons.Add(person);
            _Context.SaveChanges();
            return CreatedAtAction("GetPerson", new { id = person.Id }, person);
        }

        [HttpPut("{id}")]
        public ActionResult<Persons> putPerson(int id, Persons person)
        {
            var persons = _Context.Persons.Find(id);
            if (persons == null)
            {
                return NotFound();
            }


            persons.Naam = person.Naam;
            persons.Adres = person.Adres;
            persons.Leeftijd = person.Leeftijd;
            _Context.SaveChanges();

            return NoContent();
        }

        [HttpDelete]
        public ActionResult<Persons> deletePerson(int id)
        {
            var person = _Context.Persons.Find(id);
            if (person == null)
            {
                return NotFound();
            }

            _Context.Persons.Remove(person);
            _Context.SaveChanges();

            return NoContent();
        }

    }
}
