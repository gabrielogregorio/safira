using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace fynCode
{
    public partial class tela : Form
    {
        public tela()
        {
            InitializeComponent();
        }

        private void txt_codigo_TextChanged(object sender, EventArgs e)
        {
            txt_codigo.ForeColor = Color.Red;
        }
    }
}
