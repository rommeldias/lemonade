/**
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package br.ufmg.dcc.lemonade.ext.io;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FSDataInputStream;
import org.apache.hadoop.fs.FileStatus;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;

import java.io.IOException;
import java.io.OutputStream;

/**
 * Utility class for handle IO-related code in Lemonade.
  */
public class LemonadeFileUtil {
    /**
     * Replaces the org.apache.hadoop.fs.FileUtil implementation in order to
     * handle header inclusion.
     * Adapted to new syntax from the original available at:
     * https://dzone.com/articles/spark-write-csv-file-header
     * Adapted from code provided by Apache Software Foundation.
     *
     * @param srcFS        Source file system reference
     * @param srcDir       Source directory
     * @param dstFS        Target file system reference
     * @param dstFile      Target file
     * @param deleteSource If true, deletes the sources
     * @param conf         HDFS configuration
     * @param header       Header to be included in the final file
     * @return true if sources were deleted, false otherwise
     * @throws IOException
     */
    @SuppressWarnings("ThrowFromFinallyBlock")
    public static boolean copyMergeWithHeader(
            FileSystem srcFS, Path srcDir, FileSystem dstFS, Path dstFile,
            boolean deleteSource, Configuration conf, String header)
            throws IOException {

        dstFile = checkDest(srcDir.getName(), dstFS, dstFile, false);
        if (!srcFS.getFileStatus(srcDir).isDirectory()) {
            return false;
        } else {
            OutputStream out = dstFS.create(dstFile);
            if (header != null) {
                out.write((header + System.lineSeparator()).getBytes("UTF-8"));
            }

            try {
                FileStatus[] contents = srcFS.listStatus(srcDir);

                for (FileStatus content : contents) {
                    if (!content.isDirectory()) {

                        try (FSDataInputStream in =
                                     srcFS.open(content.getPath())) {
                            IOUtils.copyBytes(in, out, conf, false);
                        }
                    }
                }
            } finally {
                out.close();
            }

            return !deleteSource || srcFS.delete(srcDir, true);
        }
    }

    private static Path checkDest(String srcName, FileSystem dstFS, Path dst,
                                  boolean overwrite) throws IOException {
        if (dstFS.exists(dst)) {
            FileStatus status = dstFS.getFileStatus(dst);
            if (status.isDirectory()) {
                if (null == srcName) {
                    throw new IOException("Target " + dst + " is a directory");
                }
                return checkDest(null, dstFS, new Path(dst, srcName),
                        overwrite);
            }

            if (!overwrite) {
                throw new IOException("Target " + dst + " already exists");
            }
        }

        return dst;
    }
}
