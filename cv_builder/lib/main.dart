import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
// import 'package:dartpy/dartpy.dart';
// import 'dart:ffi';
// import 'package:ffi/ffi.dart';

// this text is only here to test if i can push updates to git from intiliji

void main() {
  runApp(CVBuilderApp());
}

class CVBuilderApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CV Builder',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool hasCV = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('CV Builder'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text('Do you have an existing CV?'),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      hasCV = true;
                    });
                  },
                  child: Text('Yes'),
                ),
                SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      hasCV = false;
                    });
                  },
                  child: Text('No'),
                ),
              ],
            ),
            if (hasCV) UploadCVForm(),
            if (!hasCV) NewCVForm(),
          ],
        ),
      ),
    );
  }
}

class UploadCVForm extends StatefulWidget {
  @override
  _UploadCVFormState createState() => _UploadCVFormState();
}

class _UploadCVFormState extends State<UploadCVForm> {
  final _jobDescriptionController = TextEditingController();

  Future<void> generateCVWithUpload() async {
    // Simulate a file upload and extract necessary details
    String jobDescription = _jobDescriptionController.text;
    var response = await http.post(
      Uri.parse('http://127.0.0.1:5000/generate_cv'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        'job_description': jobDescription,
        'user_info': {
          'name': 'John Doe',
          // 'email': 'john@example.com',
          // 'education': 'Bachelor of Science in Computer Science',
          'experience': '3 years of software development'
        }
      }),
    );

    if (response.statusCode == 200) {
      // print('CV generated: ${response.body}');
      print('CV generated: ');
    } else {
      print('Failed to generate CV ${response.statusCode}');
    }
    // dartpyc.Py_Initialize();
    // final python = '''
    // from time import time, ctime
    // print("Today is", ctime(time()))
    // ''';
    // final pystring = python.toNativeUtf8();
    // dartpyc.PyRun_SimpleString(pystring.cast<Char>());
    // malloc.free(pystring);
    // print(dartpyc.Py_FinalizeEx());
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Upload your CV'),
        ElevatedButton(
          onPressed: () {
            // Add file upload functionality
          },
          child: Text('Upload CV'),
        ),
        TextField(
          controller: _jobDescriptionController,
          maxLines: 5,
          decoration: InputDecoration(
            hintText: 'Job Description',
            border: OutlineInputBorder(),
          ),
        ),
        ElevatedButton(
          onPressed: generateCVWithUpload,
          child: Text('Generate CV'),
        ),
      ],
    );
  }
}


class NewCVForm extends StatefulWidget {
  @override
  _NewCVFormState createState() => _NewCVFormState();
}






class _NewCVFormState extends State<NewCVForm> {
  final _jobDescriptionController = TextEditingController();
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _educationController = TextEditingController();
  final _experienceController = TextEditingController();

  Future<void> generateNewCV() async {
    String jobDescription = _jobDescriptionController.text;
    String name = _nameController.text;
    String email = _emailController.text;
    String education = _educationController.text;
    String experience = _experienceController.text;

    var response = await http.post(
      Uri.parse('http://127.0.0.1:5000/generate_cv'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: jsonEncode(<String, dynamic>{
        'job_description': "jobDescription",
        'user_info': {
          'name': "name",
          'email': "email",
          'education': "education",
          'experience': "experience",
        }
      }),
    );

    if (response.statusCode == 200) {
      print('CV generated: ${response.body}');
    } else {
      print('Failed to generate CV ${response.statusCode}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(
          controller: _nameController,
          decoration: InputDecoration(
            hintText: 'Name',
            border: OutlineInputBorder(),
          ),
        ),
        TextField(
          controller: _emailController,
          decoration: InputDecoration(
            hintText: 'Email',
            border: OutlineInputBorder(),
          ),
        ),
        TextField(
          controller: _educationController,
          decoration: InputDecoration(
            hintText: 'Education',
            border: OutlineInputBorder(),
          ),
        ),
        TextField(
          controller: _experienceController,
          decoration: InputDecoration(
            hintText: 'Experience',
            border: OutlineInputBorder(),
          ),
        ),
        TextField(
          controller: _jobDescriptionController,
          maxLines: 5,
          decoration: InputDecoration(
            hintText: 'Job Description',
            border: OutlineInputBorder(),
          ),
        ),
        ElevatedButton(
          onPressed: generateNewCV,
          child: Text('Generate CV'),
        ),
      ],
    );
  }
}
