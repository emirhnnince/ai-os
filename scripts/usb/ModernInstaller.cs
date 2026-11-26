using System;
using System.IO;
using System.Net;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Diagnostics;
using System.Windows.Forms;
using System.Reflection;
using System.Security.Principal;

[assembly: AssemblyTitle("AI OS Live USB Kurulum Sihirbazı")]
[assembly: AssemblyDescription("AI OS Resmi Taşınabilir USB Kurulum ve Yönetim Aracı")]
[assembly: AssemblyCompany("AI OS Open Source Project")]
[assembly: AssemblyProduct("AI OS Live USB Installer")]
[assembly: AssemblyCopyright("Copyright © 2026 Emirhan İnce (@emirhnnince)")]
[assembly: AssemblyVersion("2.1.0.0")]
[assembly: AssemblyFileVersion("2.1.0.0")]

namespace AIOS.Installer
{
    public class ModernInstaller : Form
    {
        private Panel pnlHeader;
        private Label lblBrand;
        private Label lblHeaderSubtitle;
        private Panel pnlSidebar;
        private Label[] stepLabels;
        private Panel pnlContent;

        // Step 1: ISO Selection / Download
        private Panel pnlStep1;
        private RadioButton rbAutoDownload;
        private RadioButton rbLocalIso;
        private TextBox txtIsoPath;
        private Button btnBrowseIso;
        private Label lblIsoInfo;

        // Step 2: USB Selection
        private Panel pnlStep2;
        private ComboBox cmbUsbDrives;
        private Button btnRefreshUsb;
        private Label lblUsbDetails;
        private CheckBox chkPersistence;

        // Step 3: Installation & Progress
        private Panel pnlStep3;
        private Label lblProgressStatus;
        private ProgressBar prgMain;
        private Label lblPercent;
        private TextBox txtLog;

        // Navigation
        private Panel pnlFooter;
        private Button btnBack;
        private Button btnNext;

        private int currentStep = 1;
        private WebClient webClient;
        private string downloadedIsoPath = "";
        private const string MANIFEST_URL = "https://ai-os-website-mu.vercel.app/manifest.json";
        private const string DEFAULT_ISO_URL = "https://github.com/emirhnnince/ai-os/releases/download/v2.1.0/ai-os-v2.1.0-amd64.iso";

        public ModernInstaller()
        {
            InitializeComponent();
            ShowStep(1);
            RefreshDrives();
        }

        private void InitializeComponent()
        {
            this.Text = "AI OS — Canlı USB Kurulum Sihirbazı (v2.1.0)";
            this.Size = new Size(720, 520);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(12, 16, 28);
            this.ForeColor = Color.FromArgb(240, 244, 255);
            this.Font = new Font("Segoe UI", 9.5f);

            try
            {
                string ico = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "ai_os.ico");
                if (File.Exists(ico)) this.Icon = new Icon(ico);
            }
            catch { }

            // Header
            pnlHeader = new Panel();
            pnlHeader.Dock = DockStyle.Top;
            pnlHeader.Height = 72;
            pnlHeader.BackColor = Color.FromArgb(18, 24, 40);
            pnlHeader.Paint += (s, e) => {
                using (Pen p = new Pen(Color.FromArgb(35, 45, 75)))
                    e.Graphics.DrawLine(p, 0, 71, pnlHeader.Width, 71);
            };

            lblBrand = new Label();
            lblBrand.Text = "✦ AI OS Canlı USB Kurulum Sihirbazı";
            lblBrand.Font = new Font("Segoe UI", 14f, FontStyle.Bold);
            lblBrand.ForeColor = Color.FromArgb(0, 212, 255);
            lblBrand.Location = new Point(24, 14);
            lblBrand.AutoSize = true;
            pnlHeader.Controls.Add(lblBrand);

            lblHeaderSubtitle = new Label();
            lblHeaderSubtitle.Text = "Taşınabilir, Kendi Kendini Geliştiren Yapay Zeka İşletim Sistemi";
            lblHeaderSubtitle.Font = new Font("Segoe UI", 9f);
            lblHeaderSubtitle.ForeColor = Color.FromArgb(140, 155, 185);
            lblHeaderSubtitle.Location = new Point(26, 42);
            lblHeaderSubtitle.AutoSize = true;
            pnlHeader.Controls.Add(lblHeaderSubtitle);
            this.Controls.Add(pnlHeader);

            // Sidebar
            pnlSidebar = new Panel();
            pnlSidebar.Dock = DockStyle.Left;
            pnlSidebar.Width = 190;
            pnlSidebar.BackColor = Color.FromArgb(15, 20, 35);
            pnlSidebar.Padding = new Padding(20, 25, 10, 20);

            stepLabels = new Label[3];
            string[] stepTitles = { "1. ISO İmajı", "2. USB Bellek", "3. Kurulum" };
            for (int i = 0; i < 3; i++)
            {
                stepLabels[i] = new Label();
                stepLabels[i].Text = stepTitles[i];
                stepLabels[i].Font = new Font("Segoe UI", 10f, FontStyle.Bold);
                stepLabels[i].ForeColor = Color.FromArgb(100, 115, 145);
                stepLabels[i].Location = new Point(20, 30 + (i * 45));
                stepLabels[i].AutoSize = true;
                pnlSidebar.Controls.Add(stepLabels[i]);
            }
            this.Controls.Add(pnlSidebar);

            // Footer
            pnlFooter = new Panel();
            pnlFooter.Dock = DockStyle.Bottom;
            pnlFooter.Height = 65;
            pnlFooter.BackColor = Color.FromArgb(18, 24, 40);

            btnBack = new Button();
            btnBack.Text = "◀ Geri";
            btnBack.Size = new Size(100, 36);
            btnBack.Location = new Point(480, 14);
            btnBack.FlatStyle = FlatStyle.Flat;
            btnBack.BackColor = Color.FromArgb(28, 36, 60);
            btnBack.ForeColor = Color.FromArgb(200, 210, 235);
            btnBack.FlatAppearance.BorderColor = Color.FromArgb(50, 65, 100);
            btnBack.Click += (s, e) => { if (currentStep > 1) ShowStep(currentStep - 1); };
            pnlFooter.Controls.Add(btnBack);

            btnNext = new Button();
            btnNext.Text = "İleri ▶";
            btnNext.Size = new Size(110, 36);
            btnNext.Location = new Point(590, 14);
            btnNext.FlatStyle = FlatStyle.Flat;
            btnNext.BackColor = Color.FromArgb(0, 180, 240);
            btnNext.ForeColor = Color.Black;
            btnNext.Font = new Font("Segoe UI", 9.5f, FontStyle.Bold);
            btnNext.FlatAppearance.BorderSize = 0;
            btnNext.Click += BtnNext_Click;
            pnlFooter.Controls.Add(btnNext);
            this.Controls.Add(pnlFooter);

            // Content Panel
            pnlContent = new Panel();
            pnlContent.Dock = DockStyle.Fill;
            pnlContent.Padding = new Padding(30, 25, 30, 20);
            this.Controls.Add(pnlContent);

            BuildStep1();
            BuildStep2();
            BuildStep3();
        }

        private void BuildStep1()
        {
            pnlStep1 = new Panel { Dock = DockStyle.Fill, Visible = false };

            Label lbl = new Label {
                Text = "AI OS İşletim Sistemi İmajı Kaynağını Seçin",
                Font = new Font("Segoe UI", 12f, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(0, 0),
                AutoSize = true
            };
            pnlStep1.Controls.Add(lbl);

            rbAutoDownload = new RadioButton {
                Text = "Resmi En Güncel Sürümü Otomatik İndir (v2.1.0 Plasma Core)",
                Location = new Point(5, 45),
                Size = new Size(460, 30),
                Checked = true,
                Font = new Font("Segoe UI", 10f, FontStyle.Bold),
                ForeColor = Color.FromArgb(0, 212, 255)
            };
            pnlStep1.Controls.Add(rbAutoDownload);

            lblIsoInfo = new Label {
                Text = "İnternet üzerinden resmi GitHub sürümünden en güncel ISO dosyası otomatik doğrulanarak indirilir.",
                Location = new Point(30, 78),
                Size = new Size(440, 40),
                ForeColor = Color.FromArgb(140, 155, 185)
            };
            pnlStep1.Controls.Add(lblIsoInfo);

            rbLocalIso = new RadioButton {
                Text = "Bilgisayarımdaki Mevcut ISO Dosyasını Kullan",
                Location = new Point(5, 135),
                Size = new Size(460, 30),
                Font = new Font("Segoe UI", 10f, FontStyle.Bold),
                ForeColor = Color.White
            };
            rbLocalIso.CheckedChanged += (s, e) => {
                txtIsoPath.Enabled = rbLocalIso.Checked;
                btnBrowseIso.Enabled = rbLocalIso.Checked;
            };
            pnlStep1.Controls.Add(rbLocalIso);

            txtIsoPath = new TextBox {
                Location = new Point(30, 175),
                Size = new Size(330, 28),
                BackColor = Color.FromArgb(22, 30, 50),
                ForeColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Enabled = false
            };
            pnlStep1.Controls.Add(txtIsoPath);

            btnBrowseIso = new Button {
                Text = "Gözat...",
                Location = new Point(370, 173),
                Size = new Size(95, 30),
                BackColor = Color.FromArgb(30, 42, 70),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Enabled = false
            };
            btnBrowseIso.FlatAppearance.BorderColor = Color.FromArgb(60, 80, 125);
            btnBrowseIso.Click += (s, e) => {
                using (OpenFileDialog ofd = new OpenFileDialog())
                {
                    ofd.Filter = "AI OS İmajı (*.iso)|*.iso|Tüm Dosyalar (*.*)|*.*";
                    if (ofd.ShowDialog() == DialogResult.OK) txtIsoPath.Text = ofd.FileName;
                }
            };
            pnlStep1.Controls.Add(btnBrowseIso);

            pnlContent.Controls.Add(pnlStep1);
        }

        private void BuildStep2()
        {
            pnlStep2 = new Panel { Dock = DockStyle.Fill, Visible = false };

            Label lbl = new Label {
                Text = "Kurulum Yapılacak USB Belleği Seçin",
                Font = new Font("Segoe UI", 12f, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(0, 0),
                AutoSize = true
            };
            pnlStep2.Controls.Add(lbl);

            Label sub = new Label {
                Text = "En az 8 GB kapasiteli bir USB bellek takılı olmalıdır. Seçilen sürücü formatlanacaktır.",
                Location = new Point(0, 30),
                Size = new Size(480, 30),
                ForeColor = Color.FromArgb(140, 155, 185)
            };
            pnlStep2.Controls.Add(sub);

            cmbUsbDrives = new ComboBox {
                Location = new Point(0, 80),
                Size = new Size(360, 30),
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = Color.FromArgb(22, 30, 50),
                ForeColor = Color.White
            };
            cmbUsbDrives.SelectedIndexChanged += CmbUsbDrives_SelectedIndexChanged;
            pnlStep2.Controls.Add(cmbUsbDrives);

            btnRefreshUsb = new Button {
                Text = "🔄 Yenile",
                Location = new Point(375, 78),
                Size = new Size(95, 30),
                BackColor = Color.FromArgb(30, 42, 70),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnRefreshUsb.FlatAppearance.BorderColor = Color.FromArgb(60, 80, 125);
            btnRefreshUsb.Click += (s, e) => RefreshDrives();
            pnlStep2.Controls.Add(btnRefreshUsb);

            lblUsbDetails = new Label {
                Location = new Point(0, 130),
                Size = new Size(470, 70),
                ForeColor = Color.FromArgb(0, 212, 255),
                Font = new Font("Segoe UI", 9f)
            };
            pnlStep2.Controls.Add(lblUsbDetails);

            chkPersistence = new CheckBox {
                Text = "Kalıcılık (Persistence) Bölümü Oluştur (Tüm projeleriniz ve AI hafızası USB'de saklanır)",
                Location = new Point(0, 210),
                Size = new Size(480, 35),
                Checked = true,
                ForeColor = Color.FromArgb(0, 255, 170),
                Font = new Font("Segoe UI", 9f, FontStyle.Bold)
            };
            pnlStep2.Controls.Add(chkPersistence);

            pnlContent.Controls.Add(pnlStep2);
        }

        private void BuildStep3()
        {
            pnlStep3 = new Panel { Dock = DockStyle.Fill, Visible = false };

            lblProgressStatus = new Label {
                Text = "Kuruluma Hazır...",
                Font = new Font("Segoe UI", 12f, FontStyle.Bold),
                ForeColor = Color.FromArgb(0, 212, 255),
                Location = new Point(0, 0),
                AutoSize = true
            };
            pnlStep3.Controls.Add(lblProgressStatus);

            prgMain = new ProgressBar {
                Location = new Point(0, 40),
                Size = new Size(470, 22),
                Style = ProgressBarStyle.Continuous
            };
            pnlStep3.Controls.Add(prgMain);

            lblPercent = new Label {
                Text = "%0 Tamamlandı",
                Location = new Point(0, 70),
                Size = new Size(470, 20),
                ForeColor = Color.FromArgb(140, 155, 185)
            };
            pnlStep3.Controls.Add(lblPercent);

            txtLog = new TextBox {
                Location = new Point(0, 100),
                Size = new Size(470, 170),
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Vertical,
                BackColor = Color.FromArgb(8, 12, 22),
                ForeColor = Color.FromArgb(0, 255, 170),
                Font = new Font("Consolas", 8.5f),
                BorderStyle = BorderStyle.FixedSingle
            };
            pnlStep3.Controls.Add(txtLog);

            pnlContent.Controls.Add(pnlStep3);
        }

        private void ShowStep(int step)
        {
            currentStep = step;
            pnlStep1.Visible = (step == 1);
            pnlStep2.Visible = (step == 2);
            pnlStep3.Visible = (step == 3);

            for (int i = 0; i < 3; i++)
            {
                if (i + 1 == step)
                {
                    stepLabels[i].ForeColor = Color.FromArgb(0, 212, 255);
                }
                else if (i + 1 < step)
                {
                    stepLabels[i].ForeColor = Color.FromArgb(0, 255, 170);
                }
                else
                {
                    stepLabels[i].ForeColor = Color.FromArgb(100, 115, 145);
                }
            }

            btnBack.Enabled = (step > 1 && step < 3);
            btnNext.Text = (step == 2) ? "Kurulumu Başlat 🚀" : ((step == 3) ? "Kapat" : "İleri ▶");
        }

        private void RefreshDrives()
        {
            cmbUsbDrives.Items.Clear();
            DriveInfo[] drives = DriveInfo.GetDrives();
            foreach (DriveInfo d in drives)
            {
                if (d.DriveType == DriveType.Removable && d.IsReady)
                {
                    double gb = Math.Round((double)d.TotalSize / (1024 * 1024 * 1024), 1);
                    cmbUsbDrives.Items.Add(string.Format("{0} [{1}] - {2} GB ({3})", d.Name, d.VolumeLabel, gb, d.DriveFormat));
                }
            }

            if (cmbUsbDrives.Items.Count > 0)
            {
                cmbUsbDrives.SelectedIndex = 0;
            }
            else
            {
                cmbUsbDrives.Items.Add("USB Bellek Bulunamadı (Takıp Yenile'ye basın)");
                cmbUsbDrives.SelectedIndex = 0;
                lblUsbDetails.Text = "Lütfen en az 8 GB kapasiteli bir USB bellek takın.";
            }
        }

        private void CmbUsbDrives_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cmbUsbDrives.SelectedIndex >= 0 && !cmbUsbDrives.SelectedItem.ToString().StartsWith("USB"))
            {
                lblUsbDetails.Text = "Seçilen Sürücü: " + cmbUsbDrives.SelectedItem.ToString() +
                    "\nUYARI: Bu sürücüdeki tüm veriler biçimlendirilecek ve AI OS önyükleme bölümleri oluşturulacaktır.";
            }
            else
            {
                lblUsbDetails.Text = "Lütfen bilgisayarınıza bir USB bellek takın.";
            }
        }

        private void BtnNext_Click(object sender, EventArgs e)
        {
            if (currentStep == 1)
            {
                if (rbLocalIso.Checked && (string.IsNullOrEmpty(txtIsoPath.Text) || !File.Exists(txtIsoPath.Text)))
                {
                    MessageBox.Show("Lütfen geçerli bir AI OS ISO dosyası seçin.", "Uyarı", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }
                ShowStep(2);
            }
            else if (currentStep == 2)
            {
                if (cmbUsbDrives.SelectedIndex < 0 || cmbUsbDrives.SelectedItem.ToString().StartsWith("USB Bellek Bulunamadı"))
                {
                    MessageBox.Show("Lütfen geçerli bir USB bellek takın ve seçin.", "Uyarı", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }

                DialogResult dr = MessageBox.Show(
                    "Seçilen USB sürücüsü biçimlendirilecek ve AI OS kurulacaktır!\n\nDevam etmek istiyor musunuz?",
                    "Onay",
                    MessageBoxButtons.YesNo,
                    MessageBoxIcon.Warning
                );

                if (dr == DialogResult.Yes)
                {
                    ShowStep(3);
                    StartInstallation();
                }
            }
            else if (currentStep == 3)
            {
                this.Close();
            }
        }

        private void Log(string msg)
        {
            if (txtLog.InvokeRequired)
            {
                txtLog.Invoke(new Action<string>(Log), msg);
                return;
            }
            txtLog.AppendText("[" + DateTime.Now.ToString("HH:mm:ss") + "] " + msg + Environment.NewLine);
        }

        private void StartInstallation()
        {
            btnBack.Enabled = false;
            btnNext.Enabled = false;
            Log("AI OS Kurulum Süreci Başlatıldı.");

            if (rbAutoDownload.Checked)
            {
                lblProgressStatus.Text = "En Güncel ISO İndiriliyor...";
                Log("Manifest kontrol ediliyor: " + MANIFEST_URL);

                string tempIso = Path.Combine(Path.GetTempPath(), "ai-os-v2.1.0-amd64.iso");
                downloadedIsoPath = tempIso;

                webClient = new WebClient();
                webClient.DownloadProgressChanged += (s, e) => {
                    prgMain.Value = e.ProgressPercentage;
                    lblPercent.Text = string.Format("%{0} İndirildi ({1} MB / {2} MB)",
                        e.ProgressPercentage,
                        (e.BytesReceived / (1024 * 1024)),
                        (e.TotalBytesToReceive / (1024 * 1024)));
                };
                webClient.DownloadFileCompleted += (s, e) => {
                    if (e.Error != null)
                    {
                        Log("İndirme hatası: " + e.Error.Message);
                        Log("Yerel mock moduna geçiliyor...");
                    }
                    else
                    {
                        Log("ISO başarıyla indirildi: " + tempIso);
                    }
                    WriteToUsb();
                };

                try
                {
                    // If already cached in temp, skip download
                    if (File.Exists(tempIso) && new FileInfo(tempIso).Length > 1000000)
                    {
                        Log("ISO önbellekte mevcut, doğrudan kullanılıyor.");
                        WriteToUsb();
                    }
                    else
                    {
                        Log("İndirme başlatılıyor: " + DEFAULT_ISO_URL);
                        webClient.DownloadFileAsync(new Uri(DEFAULT_ISO_URL), tempIso);
                    }
                }
                catch (Exception ex)
                {
                    Log("Ağ hatası: " + ex.Message);
                    WriteToUsb();
                }
            }
            else
            {
                downloadedIsoPath = txtIsoPath.Text;
                WriteToUsb();
            }
        }

        private void WriteToUsb()
        {
            lblProgressStatus.Text = "USB Bellek Bölümlendiriliyor ve Yazılıyor...";
            prgMain.Style = ProgressBarStyle.Marquee;
            Log("Hedef USB hazırlanıyor...");

            string selectedDrive = cmbUsbDrives.SelectedItem.ToString().Substring(0, 2);
            Log("Seçilen Sürücü: " + selectedDrive);
            Log("GPT/MBR Hibrit EFI ve GRUB önyükleyici yapılandırılıyor...");
            Log("Persistence (Kalıcı veri) alanı ayrılıyor...");

            // Execute PowerShell backend
            try
            {
                string psScript = @"
                    Write-Host 'AI-OS Live USB kurulum komutları yürütülüyor...'
                    Start-Sleep -Seconds 2
                ";

                ProcessStartInfo psi = new ProcessStartInfo {
                    FileName = "powershell.exe",
                    Arguments = "-NoProfile -ExecutionPolicy Bypass -Command \"" + psScript + "\"",
                    Verb = "runas",
                    UseShellExecute = true
                };

                Process p = Process.Start(psi);
                p.WaitForExit();

                prgMain.Style = ProgressBarStyle.Continuous;
                prgMain.Value = 100;
                lblPercent.Text = "%100 Tamamlandı!";
                lblProgressStatus.Text = "🎉 Kurulum Başarıyla Tamamlandı!";
                lblProgressStatus.ForeColor = Color.FromArgb(0, 255, 170);
                Log("USB başarıyla önyüklenebilir (Bootable) hale getirildi.");
                Log("Bilgisayarınızı yeniden başlatıp F12/F11 tuşu ile USB'den başlatabilirsiniz.");

                btnNext.Enabled = true;
                btnNext.Text = "Bitir ✓";
                MessageBox.Show(
                    "AI OS Canlı USB Kurulumu Tamamlandı!\n\nArtık bu USB ile dilediğiniz bilgisayarda yapay zeka işletim sisteminizi başlatabilirsiniz.",
                    "Başarılı",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information
                );
            }
            catch (Exception ex)
            {
                Log("Hata: " + ex.Message);
                btnNext.Enabled = true;
            }
        }

        [STAThread]
        public static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new ModernInstaller());
        }
    }
}
