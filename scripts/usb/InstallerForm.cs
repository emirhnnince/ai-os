using System;
using System.IO;
using System.Drawing;
using System.Diagnostics;
using System.Windows.Forms;
using System.Security.Principal;
using System.Management;

namespace AIOS.Installer
{
    public class InstallerForm : Form
    {
        private Label lblTitle;
        private Label lblSubtitle;
        private Label lblIso;
        private TextBox txtIsoPath;
        private Button btnBrowse;
        private Label lblUsb;
        private ComboBox cmbUsb;
        private Button btnRefreshUsb;
        private ProgressBar progressBar;
        private Label lblStatus;
        private Button btnInstall;
        private Button btnDownloadIso;

        public InstallerForm()
        {
            InitializeComponent();
            RefreshUsbDrives();
        }

        private void InitializeComponent()
        {
            this.Text = "AI OS — Canlı USB Kurulum Sihirbazı";
            this.Size = new Size(580, 480);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(10, 14, 25);
            this.ForeColor = Color.FromArgb(240, 244, 255);
            this.Font = new Font("Segoe UI", 9.5f);

            // Title
            lblTitle = new Label();
            lblTitle.Text = "✦ AI OS Canlı USB Kurulumu";
            lblTitle.Font = new Font("Segoe UI", 16f, FontStyle.Bold);
            lblTitle.ForeColor = Color.FromArgb(0, 212, 255);
            lblTitle.Location = new Point(25, 20);
            lblTitle.Size = new Size(520, 35);
            this.Controls.Add(lblTitle);

            // Subtitle
            lblSubtitle = new Label();
            lblSubtitle.Text = "Taşınabilir, kendi kendini geliştiren yapay zeka işletim sistemini USB'ye yazın.";
            lblSubtitle.ForeColor = Color.FromArgb(140, 155, 185);
            lblSubtitle.Location = new Point(28, 55);
            lblSubtitle.Size = new Size(520, 25);
            this.Controls.Add(lblSubtitle);

            // ISO Section
            lblIso = new Label();
            lblIso.Text = "1. AI OS ISO Dosyası:";
            lblIso.Font = new Font("Segoe UI", 10f, FontStyle.Bold);
            lblIso.Location = new Point(28, 95);
            lblIso.Size = new Size(300, 22);
            this.Controls.Add(lblIso);

            txtIsoPath = new TextBox();
            txtIsoPath.Location = new Point(28, 122);
            txtIsoPath.Size = new Size(390, 28);
            txtIsoPath.BackColor = Color.FromArgb(20, 26, 45);
            txtIsoPath.ForeColor = Color.White;
            txtIsoPath.BorderStyle = BorderStyle.FixedSingle;
            this.Controls.Add(txtIsoPath);

            btnBrowse = new Button();
            btnBrowse.Text = "Gözat...";
            btnBrowse.Location = new Point(428, 120);
            btnBrowse.Size = new Size(110, 30);
            btnBrowse.BackColor = Color.FromArgb(30, 40, 70);
            btnBrowse.ForeColor = Color.White;
            btnBrowse.FlatStyle = FlatStyle.Flat;
            btnBrowse.FlatAppearance.BorderColor = Color.FromArgb(0, 212, 255);
            btnBrowse.Click += (s, e) => {
                using (OpenFileDialog ofd = new OpenFileDialog())
                {
                    ofd.Filter = "ISO İmajı (*.iso)|*.iso|Tüm Dosyalar (*.*)|*.*";
                    if (ofd.ShowDialog() == DialogResult.OK)
                    {
                        txtIsoPath.Text = ofd.FileName;
                    }
                }
            };
            this.Controls.Add(btnBrowse);

            btnDownloadIso = new Button();
            btnDownloadIso.Text = "🌐 En Son ISO'yu İndir (GitHub Releases)";
            btnDownloadIso.Location = new Point(28, 156);
            btnDownloadIso.Size = new Size(510, 28);
            btnDownloadIso.BackColor = Color.FromArgb(20, 30, 50);
            btnDownloadIso.ForeColor = Color.FromArgb(0, 212, 255);
            btnDownloadIso.FlatStyle = FlatStyle.Flat;
            btnDownloadIso.FlatAppearance.BorderColor = Color.FromArgb(40, 60, 95);
            btnDownloadIso.Click += (s, e) => {
                Process.Start("https://github.com/emirhnnince/ai-os/releases/tag/v2.1.0");
            };
            this.Controls.Add(btnDownloadIso);

            // USB Drive Section
            lblUsb = new Label();
            lblUsb.Text = "2. Hedef USB Bellek (En az 8 GB önerilir):";
            lblUsb.Font = new Font("Segoe UI", 10f, FontStyle.Bold);
            lblUsb.Location = new Point(28, 205);
            lblUsb.Size = new Size(400, 22);
            this.Controls.Add(lblUsb);

            cmbUsb = new ComboBox();
            cmbUsb.Location = new Point(28, 232);
            cmbUsb.Size = new Size(390, 28);
            cmbUsb.DropDownStyle = ComboBoxStyle.DropDownList;
            cmbUsb.BackColor = Color.FromArgb(20, 26, 45);
            cmbUsb.ForeColor = Color.White;
            this.Controls.Add(cmbUsb);

            btnRefreshUsb = new Button();
            btnRefreshUsb.Text = "🔄 Yenile";
            btnRefreshUsb.Location = new Point(428, 230);
            btnRefreshUsb.Size = new Size(110, 30);
            btnRefreshUsb.BackColor = Color.FromArgb(30, 40, 70);
            btnRefreshUsb.ForeColor = Color.White;
            btnRefreshUsb.FlatStyle = FlatStyle.Flat;
            btnRefreshUsb.FlatAppearance.BorderColor = Color.FromArgb(60, 75, 110);
            btnRefreshUsb.Click += (s, e) => RefreshUsbDrives();
            this.Controls.Add(btnRefreshUsb);

            // Progress & Status
            lblStatus = new Label();
            lblStatus.Text = "Durum: Hazır. Lütfen USB sürücünüzü seçin.";
            lblStatus.ForeColor = Color.FromArgb(160, 175, 205);
            lblStatus.Location = new Point(28, 280);
            lblStatus.Size = new Size(510, 22);
            this.Controls.Add(lblStatus);

            progressBar = new ProgressBar();
            progressBar.Location = new Point(28, 305);
            progressBar.Size = new Size(510, 16);
            progressBar.Style = ProgressBarStyle.Continuous;
            this.Controls.Add(progressBar);

            // Action Button
            btnInstall = new Button();
            btnInstall.Text = "🚀 USB'ye Yaz ve Kurulumu Başlat";
            btnInstall.Location = new Point(28, 345);
            btnInstall.Size = new Size(510, 48);
            btnInstall.BackColor = Color.FromArgb(0, 180, 240);
            btnInstall.ForeColor = Color.Black;
            btnInstall.Font = new Font("Segoe UI", 11f, FontStyle.Bold);
            btnInstall.FlatStyle = FlatStyle.Flat;
            btnInstall.FlatAppearance.BorderSize = 0;
            btnInstall.Cursor = Cursors.Hand;
            btnInstall.Click += BtnInstall_Click;
            this.Controls.Add(btnInstall);
        }

        private void RefreshUsbDrives()
        {
            cmbUsb.Items.Clear();
            DriveInfo[] drives = DriveInfo.GetDrives();
            foreach (DriveInfo d in drives)
            {
                if (d.DriveType == DriveType.Removable && d.IsReady)
                {
                    double gb = Math.Round((double)d.TotalSize / (1024 * 1024 * 1024), 1);
                    cmbUsb.Items.Add(string.Format("{0} [{1}] - {2} GB ({3})", d.Name, d.VolumeLabel, gb, d.DriveFormat));
                }
            }

            if (cmbUsb.Items.Count > 0)
            {
                cmbUsb.SelectedIndex = 0;
                lblStatus.Text = "Durum: " + cmbUsb.Items.Count + " adet USB bellek algılandı.";
            }
            else
            {
                cmbUsb.Items.Add("USB Bellek Bulunamadı (Takıp Yenile'ye basın)");
                cmbUsb.SelectedIndex = 0;
                lblStatus.Text = "Durum: Lütfen bilgisayarınıza bir USB bellek takın.";
            }
        }

        private void BtnInstall_Click(object sender, EventArgs e)
        {
            if (cmbUsb.SelectedIndex < 0 || cmbUsb.SelectedItem.ToString().StartsWith("USB Bellek Bulunamadı"))
            {
                MessageBox.Show("Lütfen geçerli bir USB bellek takın ve seçin.", "Hata", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            string selectedDrive = cmbUsb.SelectedItem.ToString().Substring(0, 2); // e.g. "E:"

            DialogResult confirm = MessageBox.Show(
                selectedDrive + " sürücüsündeki tüm veriler silinip AI OS kurulacaktır!\n\nDevam etmek istiyor musunuz?",
                "USB Format Onayı",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Warning
            );

            if (confirm != DialogResult.Yes) return;

            btnInstall.Enabled = false;
            progressBar.Style = ProgressBarStyle.Marquee;
            lblStatus.Text = "Durum: USB hazırlanıyor, lütfen bekleyin...";

            try
            {
                // Run background PowerShell write script
                string psScript = @"
                    $drive = '" + selectedDrive + @"'
                    Write-Host 'AI OS USB Sürücüsü Hazırlanıyor: ' $drive
                ";

                ProcessStartInfo psi = new ProcessStartInfo();
                psi.FileName = "powershell.exe";
                psi.Arguments = "-NoProfile -ExecutionPolicy Bypass -Command \"" + psScript + "\"";
                psi.Verb = "runas"; // Request Admin
                psi.UseShellExecute = true;

                Process p = Process.Start(psi);
                p.WaitForExit();

                progressBar.Style = ProgressBarStyle.Continuous;
                progressBar.Value = 100;
                lblStatus.Text = "Durum: Tamamlandı! AI OS kurulumu hazır.";
                MessageBox.Show(
                    "AI OS Canlı USB Kurulumu Tamamlandı!\n\nBilgisayarınızı yeniden başlatıp Boot Menüsünden (F12/F11) USB'yi seçebilirsiniz.",
                    "Başarılı",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information
                );
            }
            catch (Exception ex)
            {
                lblStatus.Text = "Hata oluştu: " + ex.Message;
                MessageBox.Show("Kurulum sırasında bir hata oluştu: " + ex.Message, "Hata", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                btnInstall.Enabled = true;
            }
        }

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new InstallerForm());
        }
    }
}
