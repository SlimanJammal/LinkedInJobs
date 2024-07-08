import 'package:flutter/material.dart';
import 'package:syncfusion_flutter_pdfviewer/pdfviewer.dart';
import 'dart:typed_data';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:flutter/foundation.dart' show kIsWeb;

import 'dart:html' as html;
import 'package:flutter/foundation.dart';
class PdfViewerPage extends StatelessWidget {
  final Uint8List pdfBytes;

  PdfViewerPage({required this.pdfBytes});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('PDF Viewer'),
        actions: [
          IconButton(
            icon: Icon(Icons.save),
            onPressed: () async {
              await _savePdf(context);
            },
          ),
        ],
      ),
      body: SfPdfViewer.memory(pdfBytes),
    );
  }

  Future<void> _savePdf(BuildContext context) async {
    if (kIsWeb) {
      try {
        final blob = html.Blob([pdfBytes]);
        final url = html.Url.createObjectUrlFromBlob(blob);
        final anchor = html.AnchorElement(href: url)
          ..setAttribute("download", "sample.pdf")
          ..click();
        html.Url.revokeObjectUrl(url);
      } catch (e) {
        print('Error while saving PDF: $e');
      }
    } else {
      try {

        WidgetsFlutterBinding.ensureInitialized();


        Directory documentDirectory = await getApplicationDocumentsDirectory();
        String documentPath = documentDirectory.path;


        String fullPath = '$documentPath/ss.pdf';

        File file = File(fullPath);
        await file.writeAsBytes(pdfBytes, flush: true);

        print('PDF saved successfully at: $fullPath');
      } catch (e) {
        print('Error while saving PDF: $e');
      }
    }
  }
}