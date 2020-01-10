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
            var command = _Context.Persons.FirstOrDefault(ba=>ba.Naam == naam);
            var enumerable = new[] { command };
            return enumerable;

        }

        [HttpGet("{id}")]
        public ActionResult<Persons> GetPerson(int id) {
            var command = _Context.Persons.Find(id);
            if (command == null)
            {
                return NotFound();
            }

            return command;
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
            var command = _Context.Persons.Find(id);
            if (command == null)
            {
                return NotFound();
            }


            command.Naam = person.Naam;
            command.Adres = person.Adres;
            command.Leeftijd = person.Leeftijd;
            _Context.SaveChanges();

            return NoContent();
        }

    }
}
