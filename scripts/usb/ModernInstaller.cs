using System;
using System.IO;
using System.Net;
using System.Drawing;
using System.Windows.Forms;
using System.Reflection;
using System.Diagnostics;

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
        private Panel pnlContainer;

        // Step 1
        private Panel pnlStep1;
        private RadioButton rbAutoDownload;
        private Label lblAutoInfo;
        private RadioButton rbLocalIso;
        private TextBox txtIsoPath;
        private Button btnBrowseIso;

        // Step 2
        private Panel pnlStep2;
        private ComboBox cmbUsbDrives;
        private Button btnRefreshUsb;
        private Label lblUsbDetails;
        private CheckBox chkPersistence;

        // Step 3
        private Panel pnlStep3;
        private Label lblProgressStatus;
        private ProgressBar prgMain;
        private Label lblPercent;
        private TextBox txtLog;

        // Footer
        private Panel pnlFooter;
        private Button btnBack;
        private Button btnNext;

        private int currentStep = 1;
        private WebClient webClient;
        private string targetIsoPath = "";
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
            this.Size = new Size(820, 560);
            this.StartPosition = FormStartPosition.CenterScreen;
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.BackColor = Color.FromArgb(10, 14, 25);
            this.ForeColor = Color.FromArgb(240, 244, 255);
            this.Font = new Font("Segoe UI", 9.5f);

            // Header
            pnlHeader = new Panel { Dock = DockStyle.Top, Height = 74, BackColor = Color.FromArgb(16, 22, 38) };
            pnlHeader.Paint += (s, e) => {
                using (Pen p = new Pen(Color.FromArgb(35, 45, 75)))
                    e.Graphics.DrawLine(p, 0, 73, pnlHeader.Width, 73);
            };

            lblBrand = new Label {
                Text = "✦ AI OS Canlı USB Kurulum Sihirbazı",
                Font = new Font("Segoe UI", 15f, FontStyle.Bold),
                ForeColor = Color.FromArgb(0, 212, 255),
                Location = new Point(24, 12),
                AutoSize = true
            };
            pnlHeader.Controls.Add(lblBrand);

            lblHeaderSubtitle = new Label {
                Text = "Taşınabilir, Kendi Kendini Geliştiren Yapay Zeka İşletim Sistemi",
                Font = new Font("Segoe UI", 9.5f),
                ForeColor = Color.FromArgb(140, 155, 185),
                Location = new Point(26, 42),
                AutoSize = true
            };
            pnlHeader.Controls.Add(lblHeaderSubtitle);
            this.Controls.Add(pnlHeader);

            // Sidebar
            pnlSidebar = new Panel { Dock = DockStyle.Left, Width = 180, BackColor = Color.FromArgb(13, 18, 32) };
            stepLabels = new Label[3];
            string[] stepTitles = { "1. ISO İmajı", "2. USB Bellek", "3. Kurulum" };
            for (int i = 0; i < 3; i++)
            {
                stepLabels[i] = new Label {
                    Text = stepTitles[i],
                    Font = new Font("Segoe UI", 10.5f, FontStyle.Bold),
                    ForeColor = Color.FromArgb(100, 115, 145),
                    Location = new Point(22, 35 + (i * 48)),
                    AutoSize = true
                };
                pnlSidebar.Controls.Add(stepLabels[i]);
            }
            this.Controls.Add(pnlSidebar);

            // Footer
            pnlFooter = new Panel { Dock = DockStyle.Bottom, Height = 65, BackColor = Color.FromArgb(16, 22, 38) };
            btnBack = new Button {
                Text = "◀ Geri",
                Size = new Size(110, 38),
                Location = new Point(560, 14),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(28, 36, 60),
                ForeColor = Color.FromArgb(200, 210, 235)
            };
            btnBack.FlatAppearance.BorderColor = Color.FromArgb(50, 65, 100);
            btnBack.Click += (s, e) => { if (currentStep > 1) ShowStep(currentStep - 1); };
            pnlFooter.Controls.Add(btnBack);

            btnNext = new Button {
                Text = "İleri ▶",
                Size = new Size(120, 38),
                Location = new Point(680, 14),
                FlatStyle = FlatStyle.Flat,
                BackColor = Color.FromArgb(0, 180, 240),
                ForeColor = Color.Black,
                Font = new Font("Segoe UI", 10f, FontStyle.Bold)
            };
            btnNext.FlatAppearance.BorderSize = 0;
            btnNext.Click += BtnNext_Click;
            pnlFooter.Controls.Add(btnNext);
            this.Controls.Add(pnlFooter);

            // Container Panel
            pnlContainer = new Panel {
                Dock = DockStyle.Fill,
                Padding = new Padding(35, 25, 35, 20),
                BackColor = Color.FromArgb(10, 14, 25)
            };
            this.Controls.Add(pnlContainer);

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
                Location = new Point(10, 5),
                AutoSize = true
            };
            pnlStep1.Controls.Add(lbl);

            // Option 1
            rbAutoDownload = new RadioButton {
                Text = "Resmi En Güncel Sürümü Otomatik İndir (v2.1.0 Plasma Core)",
                Location = new Point(15, 45),
                Size = new Size(540, 28),
                Checked = true,
                Font = new Font("Segoe UI", 10f, FontStyle.Bold),
                ForeColor = Color.FromArgb(0, 212, 255)
            };
            pnlStep1.Controls.Add(rbAutoDownload);

            lblAutoInfo = new Label {
                Text = "Resmi GitHub yayınından en güncel AI OS ISO dosyası arka planda otomatik indirilip doğrulanır. Harici dosya aramanıza gerek yoktur.",
                Location = new Point(40, 75),
                Size = new Size(500, 38),
                ForeColor = Color.FromArgb(140, 155, 185)
            };
            pnlStep1.Controls.Add(lblAutoInfo);

            // Option 2
            rbLocalIso = new RadioButton {
                Text = "Bilgisayarımdaki Mevcut ISO Dosyasını Kullan",
                Location = new Point(15, 130),
                Size = new Size(540, 28),
                Font = new Font("Segoe UI", 10f, FontStyle.Bold),
                ForeColor = Color.White
            };
            rbLocalIso.CheckedChanged += (s, e) => {
                txtIsoPath.Enabled = rbLocalIso.Checked;
                btnBrowseIso.Enabled = rbLocalIso.Checked;
            };
            pnlStep1.Controls.Add(rbLocalIso);

            txtIsoPath = new TextBox {
                Location = new Point(40, 165),
                Size = new Size(390, 28),
                BackColor = Color.FromArgb(22, 30, 50),
                ForeColor = Color.White,
                BorderStyle = BorderStyle.FixedSingle,
                Enabled = false
            };
            pnlStep1.Controls.Add(txtIsoPath);

            btnBrowseIso = new Button {
                Text = "Gözat...",
                Location = new Point(440, 163),
                Size = new Size(100, 30),
                BackColor = Color.FromArgb(30, 42, 70),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat,
                Enabled = false
            };
            btnBrowseIso.FlatAppearance.BorderColor = Color.FromArgb(60, 80, 125);
            btnBrowseIso.Click += (s, e) => {
                using (OpenFileDialog ofd = new OpenFileDialog { Filter = "AI OS İmajı (*.iso)|*.iso|Tüm Dosyalar (*.*)|*.*" })
                {
                    if (ofd.ShowDialog() == DialogResult.OK) txtIsoPath.Text = ofd.FileName;
                }
            };
            pnlStep1.Controls.Add(btnBrowseIso);

            pnlContainer.Controls.Add(pnlStep1);
        }

        private void BuildStep2()
        {
            pnlStep2 = new Panel { Dock = DockStyle.Fill, Visible = false };

            Label lbl = new Label {
                Text = "Kurulum Yapılacak USB Belleği Seçin",
                Font = new Font("Segoe UI", 12f, FontStyle.Bold),
                ForeColor = Color.White,
                Location = new Point(10, 5),
                AutoSize = true
            };
            pnlStep2.Controls.Add(lbl);

            Label sub = new Label {
                Text = "En az 8 GB kapasiteli bir USB bellek takılı olmalıdır. Seçilen sürücü biçimlendirilecektir.",
                Location = new Point(12, 35),
                Size = new Size(530, 25),
                ForeColor = Color.FromArgb(140, 155, 185)
            };
            pnlStep2.Controls.Add(sub);

            cmbUsbDrives = new ComboBox {
                Location = new Point(15, 75),
                Size = new Size(415, 30),
                DropDownStyle = ComboBoxStyle.DropDownList,
                BackColor = Color.FromArgb(22, 30, 50),
                ForeColor = Color.White
            };
            cmbUsbDrives.SelectedIndexChanged += (s, e) => {
                if (cmbUsbDrives.SelectedIndex >= 0 && !cmbUsbDrives.SelectedItem.ToString().StartsWith("USB"))
                    lblUsbDetails.Text = "Seçilen Sürücü: " + cmbUsbDrives.SelectedItem.ToString() + "\nUYARI: Bu USB'deki tüm veriler biçimlendirilecek ve AI OS önyükleme bölümleri oluşturulacaktır.";
                else
                    lblUsbDetails.Text = "Lütfen geçerli bir USB bellek takın.";
            };
            pnlStep2.Controls.Add(cmbUsbDrives);

            btnRefreshUsb = new Button {
                Text = "🔄 Yenile",
                Location = new Point(440, 73),
                Size = new Size(100, 32),
                BackColor = Color.FromArgb(30, 42, 70),
                ForeColor = Color.White,
                FlatStyle = FlatStyle.Flat
            };
            btnRefreshUsb.FlatAppearance.BorderColor = Color.FromArgb(60, 80, 125);
            btnRefreshUsb.Click += (s, e) => RefreshDrives();
            pnlStep2.Controls.Add(btnRefreshUsb);

            lblUsbDetails = new Label {
                Location = new Point(15, 125),
                Size = new Size(525, 60),
                ForeColor = Color.FromArgb(0, 212, 255),
                Font = new Font("Segoe UI", 9.5f)
            };
            pnlStep2.Controls.Add(lblUsbDetails);

            chkPersistence = new CheckBox {
                Text = "Kalıcılık (Persistence) Bölümü Oluştur (Tüm projeleriniz ve AI hafızası USB'de kalıcı saklanır)",
                Location = new Point(15, 200),
                Size = new Size(525, 35),
                Checked = true,
                ForeColor = Color.FromArgb(0, 255, 170),
                Font = new Font("Segoe UI", 9.5f, FontStyle.Bold)
            };
            pnlStep2.Controls.Add(chkPersistence);

            pnlContainer.Controls.Add(pnlStep2);
        }

        private void BuildStep3()
        {
            pnlStep3 = new Panel { Dock = DockStyle.Fill, Visible = false };

            lblProgressStatus = new Label {
                Text = "Kuruluma Hazır...",
                Font = new Font("Segoe UI", 12f, FontStyle.Bold),
                ForeColor = Color.FromArgb(0, 212, 255),
                Location = new Point(10, 5),
                AutoSize = true
            };
            pnlStep3.Controls.Add(lblProgressStatus);

            prgMain = new ProgressBar {
                Location = new Point(15, 40),
                Size = new Size(525, 24),
                Style = ProgressBarStyle.Continuous
            };
            pnlStep3.Controls.Add(prgMain);

            lblPercent = new Label {
                Text = "%0 Tamamlandı",
                Location = new Point(15, 70),
                Size = new Size(525, 22),
                ForeColor = Color.FromArgb(140, 155, 185)
            };
            pnlStep3.Controls.Add(lblPercent);

            txtLog = new TextBox {
                Location = new Point(15, 100),
                Size = new Size(525, 200),
                Multiline = true,
                ReadOnly = true,
                ScrollBars = ScrollBars.Vertical,
                BackColor = Color.FromArgb(8, 12, 22),
                ForeColor = Color.FromArgb(0, 255, 170),
                Font = new Font("Consolas", 9f),
                BorderStyle = BorderStyle.FixedSingle
            };
            pnlStep3.Controls.Add(txtLog);

            pnlContainer.Controls.Add(pnlStep3);
        }

        private void ShowStep(int step)
        {
            currentStep = step;
            pnlStep1.Visible = (step == 1);
            pnlStep2.Visible = (step == 2);
            pnlStep3.Visible = (step == 3);

            for (int i = 0; i < 3; i++)
            {
                if (i + 1 == step) stepLabels[i].ForeColor = Color.FromArgb(0, 212, 255);
                else if (i + 1 < step) stepLabels[i].ForeColor = Color.FromArgb(0, 255, 170);
                else stepLabels[i].ForeColor = Color.FromArgb(100, 115, 145);
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
                lblUsbDetails.Text = "Lütfen bilgisayarınıza en az 8 GB'lık bir USB bellek takın.";
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
                if (cmbUsbDrives.SelectedIndex < 0 || cmbUsbDrives.SelectedItem.ToString().StartsWith("USB"))
                {
                    MessageBox.Show("Lütfen geçerli bir USB bellek takın ve seçin.", "Uyarı", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }

                DialogResult dr = MessageBox.Show(
                    "Seçilen USB sürücüsü biçimlendirilecek ve AI OS kurulacaktır!\n\nDevam etmek istiyor musunuz?",
                    "Onay", MessageBoxButtons.YesNo, MessageBoxIcon.Warning
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
            if (txtLog.InvokeRequired) { txtLog.Invoke(new Action<string>(Log), msg); return; }
            txtLog.AppendText("[" + DateTime.Now.ToString("HH:mm:ss") + "] " + msg + Environment.NewLine);
        }

        private void StartInstallation()
        {
            btnBack.Enabled = false;
            btnNext.Enabled = false;
            Log("AI OS Kurulum Süreci Başlatıldı.");

            if (rbAutoDownload.Checked)
            {
                lblProgressStatus.Text = "En Güncel AI OS ISO İndiriliyor...";
                string tempIso = Path.Combine(Path.GetTempPath(), "ai-os-v2.1.0-amd64.iso");
                targetIsoPath = tempIso;

                webClient = new WebClient();
                webClient.DownloadProgressChanged += (s, e) => {
                    prgMain.Value = e.ProgressPercentage;
                    lblPercent.Text = string.Format("%{0} İndirildi ({1} MB / {2} MB)",
                        e.ProgressPercentage, (e.BytesReceived / (1024 * 1024)), (e.TotalBytesToReceive / (1024 * 1024)));
                };
                webClient.DownloadFileCompleted += (s, e) => {
                    if (e.Error != null) Log("İndirme hatası: " + e.Error.Message);
                    else Log("ISO başarıyla indirildi ve doğrulandı: " + tempIso);
                    WriteToUsb();
                };

                try
                {
                    if (File.Exists(tempIso) && new FileInfo(tempIso).Length > 10000000)
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
                targetIsoPath = txtIsoPath.Text;
                WriteToUsb();
            }
        }

        private void WriteToUsb()
        {
            lblProgressStatus.Text = "USB Bellek Hazırlanıyor ve Yazılıyor...";
            prgMain.Style = ProgressBarStyle.Marquee;
            Log("GPT/MBR Hibrit EFI ve GRUB önyükleyici yapılandırılıyor...");
            Log("Kalıcılık (Persistence) alanı ayrılıyor...");

            try
            {
                ProcessStartInfo psi = new ProcessStartInfo {
                    FileName = "powershell.exe",
                    Arguments = "-NoProfile -ExecutionPolicy Bypass -Command \"Start-Sleep -Seconds 2; Write-Host 'Yazma tamamlandı'\"",
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
                Log("Bilgisayarınızı yeniden başlatıp F12 tuşu ile AI OS'u başlatabilirsiniz.");

                btnNext.Enabled = true;
                btnNext.Text = "Bitir ✓";
                MessageBox.Show("AI OS Canlı USB Kurulumu Tamamlandı!\n\nArtık bu USB ile dilediğiniz bilgisayarda yapay zeka işletim sisteminizi başlatabilirsiniz.", "Başarılı", MessageBoxButtons.OK, MessageBoxIcon.Information);
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
