using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace testApiMac.Model
{
    public partial class Persons
    {
        [Key]
        public int Id { get; set; }
        [Required]
        [StringLength(255)]
        public string Naam { get; set; }
        [StringLength(255)]
        public string Adres { get; set; }
        public int? Leeftijd { get; set; }
    }
}
