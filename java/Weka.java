import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Random;

import weka.classifiers.Evaluation;
import weka.classifiers.functions.LibSVM;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ArffLoader;
import weka.core.converters.ArffSaver;
import weka.core.converters.ConverterUtils.DataSource;


public class Weka {
	public static void main(String [] args){
		String input_path = "./train.txt";
		if( args.length == 2)
			input_path = args[1];
		
		try {
			//DataSource source = new DataSource("./train/cpu.arff");
		
		Instances data ; 
		FastVector atts = new FastVector(); 
		FastVector  attVals = new FastVector();
        attVals.addElement("1");
        attVals.addElement("-1");
        //attVals.addElement("0");
        int len = 0;
        File tmp = new File(input_path);
		if(tmp != null){
			try {
				BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(tmp), "UTF-8"));	
				String line = null;
				while ((line = reader.readLine()) != null) {			
					len = line.trim().split("\\s+").length;
					if( len>0)
						break;
				}
				reader.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		}
		
		for(int i =0 ;i < len; i++){
			if( i == 0 )
				atts.addElement(new Attribute("class", attVals));
			else
				atts.addElement(new Attribute("index" + i));
		}
		data = new Instances("data", atts, 0);  
			
		
		File file = new File(input_path);
		if(file != null){
			try {
				BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file), "UTF-8"));	
				String line = null;
				while ((line = reader.readLine()) != null) {			
					if (line.isEmpty() || line.startsWith("#"))
						continue;
					String[] a = line.trim().split("\\s+");
					int length = a.length;				
					double value[] = new double[length];
					for(int i = 0;i < length ;i++){
						
						if( i == 0)
						{	double d = Double.parseDouble(a[i]);
						
							if(d == 1.0)
								value[i]  = attVals.indexOf("1");
							else if( d == -1.0)
								value[i]  = attVals.indexOf("-1");
							
						}
						else{
							String[] t = a[i].split(":");
							//int dd =  Integer.parseInt(a[i].split(":")[0]);	
							if( t.length == 1 )
								value[i] = Double.parseDouble(a[i].split(":")[0]); 
							else
								value[i] = Double.parseDouble(a[i].split(":")[1]); 

						}
						
					}
					data.add(new Instance(1.0,value));
				}				
				reader.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		}
		data.setClassIndex(0);
			
//		ArffSaver saver = new ArffSaver();  
//	    saver.setInstances(data);  
//	    saver.setFile(new File("./train.arff"));  
//	    saver.writeBatch();
//	    System.out.println("arff生成完成!");
		
		LibSVM svm = new LibSVM();
//		String[] options = svm.getOptions();
//		for(int i = 0;i<options.length;i++)
//		System.out.println(		options[i]);
		//svm.buildClassifier(data);
		
		Evaluation eval=null;
		
		eval=new Evaluation(data);
		eval.crossValidateModel(svm, data, 10, new Random(1));//
		
		System.out.println(eval.toSummaryString());//
		System.out.println(eval.toClassDetailsString());//
		System.out.println(eval.toMatrixString());//
		
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
