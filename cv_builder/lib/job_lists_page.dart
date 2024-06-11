import 'dart:convert';
import 'dart:io';
// import 'dart:nativewrappers/_internal/vm/lib/typed_data_patch.dart';
import 'dart:typed_data';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_pdfview/flutter_pdfview.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'cv_pdf.dart';
class JobsPage extends StatefulWidget {
  const JobsPage({super.key});

  @override
  State<StatefulWidget> createState() => _JobsPageState();
}


class PDFViewPage extends StatelessWidget {
  final String path;

  PDFViewPage(this.path);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('View CV'),
        leading: IconButton(
          icon: Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.download),
            onPressed: () async {
              // 1. Get the existing file path
              final filePath = path; // Assuming 'path' variable holds the existing file path

              // 2. Get file name from existing path (optional)
              final fileName = filePath.split('/').last; // Get last segment (filename)

              // 3. Open file picker for saving
              final result = await FilePicker.platform.saveFile(
                dialogTitle: 'Save File',
                initialDirectory: fileName, // Pre-fill with original filename (optional)
              );

              if (result != null) {
                // 4. Access the chosen path correctly
                final newSavePath = result; // Access the path directly

                await File(filePath).copy(newSavePath);

                // 5. Show success message
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('File saved successfully!'),
                  ),
                );
              } else {
                // 6. User canceled or error (optional)
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('File saving cancelled.'),
                  ),
                );
              }
            },
          ),
        ],
      ),
      body: SfPdfViewer.file(File(path)),

    );
  }
}



class _JobsPageState extends State<JobsPage> {
  final _jobDescriptionController = TextEditingController();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _educationController = TextEditingController();
  final _experienceController = TextEditingController();
  final _linkedinController = TextEditingController();
  final _githubController = TextEditingController();
  final _phoneNumberController = TextEditingController();
  final _addressController = TextEditingController();
  final _careerObjectiveController = TextEditingController();
  final _degreeController = TextEditingController();
  final _institutionController = TextEditingController();
  final _yearsInEducationController = TextEditingController();
  final _educationDetailsController = TextEditingController();
  final _jobTitleController = TextEditingController();
  final _companyController = TextEditingController();
  final _locationController = TextEditingController();
  final _experienceYearsController = TextEditingController();
  final _responsibilitiesController = TextEditingController();
  final _skillsController = TextEditingController();
  final _certificateNameController = TextEditingController();
  final _certificateInstitutionController = TextEditingController();
  final _certificateyearController = TextEditingController();
  final _projectNameController = TextEditingController();
  final _projectDescriptionController = TextEditingController();
  final _awardNameController = TextEditingController();
  final _awardInstitutionController = TextEditingController();
  final _awardyearController = TextEditingController();
  final _organizationNameController = TextEditingController();
  final _roleController = TextEditingController();
  final _affiliationyearController = TextEditingController();

  Future<void> clearfields() async{

      // Clear all user info controllers
      _jobDescriptionController.clear();
      _nameController.clear();
      _emailController.clear();
      _phoneNumberController.clear();
      _addressController.clear();
      _linkedinController.clear();
      _githubController?.clear(); // Clear if not null
      _careerObjectiveController.clear();

      // Clear education controllers
      _degreeController.clear();
      _institutionController.clear();
      _yearsInEducationController.clear();
      _educationDetailsController.clear();

      // Clear work experience controllers
      _jobTitleController.clear();
      _companyController.clear();
      _locationController.clear();
      _experienceYearsController.clear();
      _responsibilitiesController.clear();

      // Clear skills controller
      _skillsController.clear();

      // Clear certificate controllers
      _certificateNameController.clear();
      _certificateInstitutionController.clear();
      _certificateyearController.clear();

      // Clear project controllers
      _projectNameController.clear();
      _projectDescriptionController.clear();

      // Clear award controllers
      _awardNameController.clear();
      _awardInstitutionController.clear();
      _awardyearController.clear();

      // Clear professional affiliation controllers
      _organizationNameController.clear();
      _roleController.clear();
      _affiliationyearController.clear();


  }

  Future<void> generateNewCV() async {
    String jobDescription = _jobDescriptionController.text;
    String name = _nameController.text;
    String email = _emailController.text;
    String phoneNumber = _phoneNumberController.text;
    String address = _addressController.text;
    String linkedinProfile = _linkedinController.text;
    String githubProfile = _githubController.text;
    String careerObjective = _careerObjectiveController.text;
    String degree = _degreeController.text;
    String institution = _institutionController.text;
    String years = _yearsInEducationController.text;
    String details = _educationDetailsController.text;

// For experience fields
    String jobTitle = _jobTitleController.text;
    String company = _companyController.text;
    String location = _locationController.text;
    String experienceYears = _experienceYearsController.text; // Assuming 'years' refers to experience years
    String responsibilities = _responsibilitiesController.text;

// For skills
    String skills = _skillsController.text;

// For certificates
    String certificateName = _certificateNameController.text;
    String certificateInstitution = _certificateInstitutionController.text;
    String certificateyear = _certificateyearController.text;
// For projects
    String projectName = _projectNameController.text;
    String projectDescription = _projectDescriptionController.text;


// For awards
    String awardName = _awardNameController.text;
    String aawardInstitution = _awardInstitutionController.text;
    String awardyear = _awardyearController.text;


//proffesional affeliationa
    String orginizationName = _organizationNameController.text;
    String role = _roleController.text;
    String affiliationyear = _affiliationyearController.text;
    Uint8List? pdfBytes;






    Future<void> _viewPDF(Uint8List pdfBytes) async {
      // Get the temporary directory
      final dir = await getTemporaryDirectory();
      // Create a temporary file
      final file = File('${dir.path}/resume.pdf');
      // Write the PDF bytes to the file
      await file.writeAsBytes(pdfBytes, flush: true);

      // Navigate to the PDF view page
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PDFViewPage(file.path),
        ),
      );
    }

    var response = await http.post(
      Uri.parse('http://127.0.0.1:5000/generate_cv'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        "job_description": jobDescription,
        "user_info": {
          "full_name": name,
          "email": email,
          "phone": phoneNumber,
          "address": address,
          "linkedin": linkedinProfile,
          "career_objective": careerObjective,
          "education": [
            {
              "degree": degree,
              "institution": institution,
              "years": years,
              "details": details
            }//,
            // {
            //   "degree": "M.Sc. in Software Engineering",
            //   "institution": "Example Institute of Technology",
            //   "years": "2019-2021",
            //   "details": "Thesis on machine learning algorithms..."
            // }
          ],
          "work_experience": [
            {
              "job_title": jobTitle,
              "company": company,
              "location": location,
              "years": experienceYears,
              "responsibilities": responsibilities
            }
          ],
          "skills": [
            skills
          ],
          "certifications": [
            {
              "name": certificateName,
              "institution": certificateInstitution,
              "year": certificateyear
            }
          ],
          "projects": [
            {
              "name": projectName,
              "description": projectDescription
            }//,
            // {
            //   "name": "Machine Learning Model for Predicting Stock Prices",
            //   "description": "Developed a predictive model using Python and scikit-learn..."
            // }
          ],
          "awards": [
            {
              "name": awardName,
              "institution": aawardInstitution,
              "year": awardyear
            }
          ],
          "professional_affiliations": [
            {
              "organization": orginizationName,
              "role": role,
              "years": affiliationyear
            }
          ],
          "references": []
        }
      }),
    );

    if (response.statusCode == 200) {
      setState(() {
        pdfBytes = response.bodyBytes as Uint8List?;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('CV generated successfully!'),
        ),
      );
      if (pdfBytes != null) {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => PdfViewerPage(pdfBytes: pdfBytes!),
          ),
        );
      }
    } else {
      print('Failed to generate CV ${response.statusCode}');
    }

  }







  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.cyan,
          title: Text('Jobs'),
          leading: BackButton(
            onPressed: () => Navigator.pop(context),
          ),
        ),
      drawer: Drawer(backgroundColor: Colors.blue),
      body: NestedScrollView(
        headerSliverBuilder: (context, innerBoxIsScrolled) => [
          // SliverAppBar(
            // title: TabBar(
            //   tabs: [
            //     Tab(icon: Icon(Icons.code)),
            //     Tab(icon: Icon(Icons.add_chart_sharp)),
            //     Tab(icon: Icon(Icons.accessibility)),
            //   ],
            // ),
          // ),
        ],
        body: SingleChildScrollView(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              children: [
                SizedBox(height: 28),
                Text('Personal Info'),
                SizedBox(height: 28),
                TextField(
                  controller: _nameController,
                  decoration: InputDecoration(
                    hintText: 'Full Name',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _emailController,
                  decoration: InputDecoration(
                    hintText: 'Email',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _phoneNumberController,
                  decoration: InputDecoration(
                    hintText: 'Phone Number',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _addressController,
                  decoration: InputDecoration(
                    hintText: 'Adress',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _linkedinController,
                  decoration: InputDecoration(
                    hintText: 'LinkedIn Profile',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _careerObjectiveController,
                  decoration: InputDecoration(
                    hintText: 'Career Objective',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _jobDescriptionController,
                  maxLines: 5,
                  decoration: InputDecoration(
                    hintText: 'Job Description',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 28),
                Text('Education info'),
                SizedBox(height: 28),
                TextField(
                  controller: _degreeController,
                  decoration: InputDecoration(
                    hintText: 'Degree',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _institutionController,
                  decoration: InputDecoration(
                    hintText: 'Study Institution',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _yearsInEducationController,
                  decoration: InputDecoration(
                    hintText: 'Education Timeline (i.e 2022-present)',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _educationDetailsController,
                  maxLines: 5,
                  decoration: InputDecoration(
                    hintText: 'More about your education',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 28),
                Text('Work Experience'),
                SizedBox(height: 28),
                TextField(
                  controller: _jobTitleController,
                  decoration: InputDecoration(
                    hintText: 'job title',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _companyController,
                  // maxLines: 5,
                  decoration: InputDecoration(
                    hintText: 'Company name',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _locationController,
                  decoration: InputDecoration(
                    hintText: 'job location',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _experienceYearsController,
                  decoration: InputDecoration(
                    hintText: 'Years of employment',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _responsibilitiesController,
                  decoration: InputDecoration(
                    hintText: 'responsibilities',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _skillsController,
                  decoration: InputDecoration(
                    hintText: 'List Relevant skills you have',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 28),
                Text('Certificates'),
                SizedBox(height: 28),
                TextField(
                  controller: _certificateNameController,
                  decoration: InputDecoration(
                    hintText: 'Cirtificate title',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _certificateInstitutionController,
                  decoration: InputDecoration(
                    hintText: 'Certificate provider i.e. google/IBM',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _certificateyearController,
                  decoration: InputDecoration(
                    hintText: 'When did you get the certificate',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 28),
                Text('Projects'),
                SizedBox(height: 28),
                TextField(
                  controller: _projectNameController,
                  decoration: InputDecoration(
                    hintText: 'project title',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _projectDescriptionController,
                  maxLines: 5,
                  decoration: InputDecoration(
                    hintText: 'Project Description',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 28),
                Text('Awards'),
                SizedBox(height: 28),
                TextField(
                  controller: _awardNameController,
                  decoration: InputDecoration(
                    hintText: 'Award title',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _awardInstitutionController,
                  decoration: InputDecoration(
                    hintText: 'Award institution',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _awardyearController,
                  decoration: InputDecoration(
                    hintText: 'When did you get the Award',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 28),
                Text('professional affeliation'),
                SizedBox(height: 28),
                TextField(
                  controller: _organizationNameController,
                  decoration: InputDecoration(
                    hintText: 'Orginization name',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _roleController,
                  decoration: InputDecoration(
                    hintText: 'What part did you play?',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 8),
                TextField(
                  controller: _affiliationyearController,
                  decoration: InputDecoration(
                    hintText: 'Timeline',
                    border: OutlineInputBorder(),
                  ),
                ),
                SizedBox(height: 16),
                Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                  ElevatedButton(
                    onPressed: generateNewCV,
                    child: Text('Generate CV'),
                  ),
                  ElevatedButton(
                    onPressed: clearfields,
                    child: Text('clear all'),
                  ),
                ]

                ),

              ],
            ),
          ),
        ),
      ),
    );
  }
}
